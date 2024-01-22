from autogen.agentchat.contrib.teachable_agent import TeachableAgent

try:
    from termcolor import colored
except ImportError:

    def colored(x, *args, **kwargs):
        return x


class MessageExtractionAgent(TeachableAgent):

    def consider_memo_storage(self, comment):
        """Decides whether to store something from one user comment in the DB."""
        # Check for broad CRM-related information.
        response = self.analyze(
            comment,
            """Does the TEXT include any details that are important 
            for understanding for parsing property details, like address,
            name, amenities, landmark, price, type of property? 
            Respond with yes or no.""",
        )
        if "yes" in response.lower():
            # Extract all relevant Property information.
            prop_info = self.analyze(
                comment,
                """Extract all details from the TEXT that are important for
                Property, including any mentions of address, part of address,
                amenities, building name, rental / sale detail
                or other relevant details.""",
            )
            if prop_info.strip():
                # Formulate a schema this text is containing.
                question = self.analyze(
                    comment,
                    "If you had to store the TEXT in json format, what will be the schema you will choose.Provide the schema or json keys only.",
                )
                # Store the Property information as a memo.
                if self.verbosity >= 1:
                    print(colored("\nREMEMBER THIS PROPERTY INFORMATION", "light_yellow"))
                self.memo_store.add_input_output_pair(question, prop_info)

    def consider_memo_retrieval(self, comment):
        """Decides whether to retrieve memos from the DB, and add them to the chat context."""
        # Directly use the user comment for memo retrieval.
        memo_list = self.retrieve_relevant_memos(comment)

        # Additional CRM-specific check.
        response = self.analyze(
            comment,
            "Does the TEXT request information on any property or details related to property? Answer with yes or no.",
        )
        if "yes" in response.lower():
            # Retrieve relevant CRM memos.
            crm_query = "What kind of details are requested and preferences provided, or specific needs based on previous interactions?"
            memo_list.extend(self.retrieve_relevant_memos(crm_query))

        # De-duplicate the memo list.
        memo_list = list(set(memo_list))

        # Append the memos to the last user message.
        return comment + self.concatenate_memo_texts(memo_list)