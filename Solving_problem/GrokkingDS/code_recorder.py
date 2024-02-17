def code_recorder():
    import streamlit as st
    import pathlib
    import json

    folder = pathlib.Path(__file__).parent.resolve()
    file_json = folder / "code_implementation.json"
    expandall = st.checkbox(label='Show Code')

    try:
        with open(file_json, 'r') as implm:
            data = json.load(implm)
        algo_dict = {row['algo']: ind for ind, row in enumerate(data)}
        select_algo = st.selectbox(label="Algos",
                                options=list(algo_dict.keys()))
        row = data[algo_dict[select_algo]]

        st.markdown(f""" #### Datastructure / Algorithm: {row['algo']}""")
        if row['supp_class'] != 'None':
            with st.expander(label=row['supp_class'],
                            expanded=expandall):
                st.code(body=row['supp_code'])
        with st.expander(label=row['main_class'],
                        expanded=expandall):
            st.code(body=row['init_code'])
        for method in row["methods"]:
            with st.expander(label=method['name'],
                            expanded=expandall):
                st.code(body=method['code'])
    except Exception as e:
        st.write(f"Work on new file:  {e}")

    st.markdown("#### Add New Algorithm Code:")
    with st.expander("Add New Algo"):
        algo = st.text_input(label="Algo/DS",
                            value="DS or Algo Name")
        supp_class = st.text_input(label="Support Class",
                                value="Name of Class")
        supp_code = st.text_area(label="Support Class code",
                                value="Paste the code here")

        algo_class = st.text_input(label="Main Class init",
                                value="Name of Class")
        init_code = st.text_area(label="Main Class code",
                                value="Paste the code here")
        num_methods = int(st.text_input(label="How Many Methods",
                                        value=1))

        methods = []
        for meth in range(num_methods):
            meth_name = st.text_input(label="method_name",
                                    value="Method Name",
                                    key=meth)
            meth_code = st.text_area(label="method_code",
                                    value="Paste the code here",
                                    key=meth+num_methods)
            method_data = {"name": meth_name,
                        "code": meth_code}
            methods.append(method_data)


        submit = st.button("submit")
        if submit:
            main_data = {
                "algo": algo,
                "supp_class": supp_class,
                "supp_code": supp_code,
                "main_class": algo_class,
                "init_code": init_code,
                "num_methods": num_methods,
                "methods": methods
                }

            try:
                data.append(main_data)
                st.write(len(data))
                with open(file_json, 'w') as updt:
                    json.dump(data, updt)
            except Exception as e:
                data = [main_data]
                with open(file_json, 'w') as updt:
                    json.dump(data, updt)
                print(e)
        file_name = st.text_input(label="Filename with extension",
                                value="Provide Filename")
        with open(file_json, 'r') as out:
            st.download_button(label="Save File",
                            data=out,
                            mime="application/json",
                            file_name=file_name)