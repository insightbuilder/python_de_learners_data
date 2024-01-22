from autogen.agentchat.contrib.teachable_agent import TeachableAgent

try:
    from termcolor import colored
except ImportError:

    def colored(x, *args, **kwargs):
        return x


class CustomTeachableAgent(TeachableAgent):

    def consider_memo_storage(self, comment):
        """Decides whether to store something from one user comment in the DB."""
        # Check for broad CRM-related information.
        response = self.analyze(
            comment,
            "Does the TEXT include any details that are important for understanding customer needs, preferences, or intentions, such as product interest or timeline? Respond with yes or no.",
        )
        if "yes" in response.lower():
            # Extract all relevant CRM information.
            crm_info = self.analyze(
                comment,
                "Extract all details from the TEXT that are important for CRM, including any mentions of product preferences, customer intentions, timeframes, or other relevant details.",
            )
            if crm_info.strip():
                # Formulate a question this information could answer.
                question = self.analyze(
                    comment,
                    "If someone asked for a summary of this customer's needs or preferences based on the TEXT, what question would they be asking? Provide the question only.",
                )
                # Store the CRM information as a memo.
                if self.verbosity >= 1:
                    print(colored("\nREMEMBER THIS CRM INFORMATION", "light_yellow"))
                self.memo_store.add_input_output_pair(question, crm_info)

    def consider_memo_retrieval(self, comment):
        """Decides whether to retrieve memos from the DB, and add them to the chat context."""
        # Directly use the user comment for memo retrieval.
        memo_list = self.retrieve_relevant_memos(comment)

        # Additional CRM-specific check.
        response = self.analyze(
            comment,
            "Does the TEXT request information on a customer's product preferences, intentions, or specific needs? Answer with yes or no.",
        )
        if "yes" in response.lower():
            # Retrieve relevant CRM memos.
            crm_query = "What are the customer's product preferences or specific needs based on previous interactions?"
            memo_list.extend(self.retrieve_relevant_memos(crm_query))

        # De-duplicate the memo list.
        memo_list = list(set(memo_list))

        # Append the memos to the last user message.
        return comment + self.concatenate_memo_texts(memo_list)