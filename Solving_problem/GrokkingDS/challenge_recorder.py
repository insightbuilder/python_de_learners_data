def challenge_rec():
    import streamlit as st
    import pathlib
    import json
    from datetime import datetime

    folder = pathlib.Path(__file__).parent.resolve()
    file_json = folder / "errors_hints.json"
    try:
        with open(file_json, 'r') as chlng:
            data = json.load(chlng)

        for ind, row in enumerate(data):
            st.markdown(f""" #### Date: {row['date']}""")
            st.markdown(f"Day: {row['day']}")
            st.markdown("#### Challenges: ")
            for pt in row['points']:
                st.write(pt)
            remove_row = st.button(label='Remove Data',
                                   key=ind)
            if remove_row:
                data.pop(ind)
                with open(file_json, 'w') as updt:
                    json.dump(data, updt)
                    st.write("Data File updated.")
                st.rerun()
    except Exception as e:
        st.write(f"Work on new file:  {e}")

    today = st.date_input(label="Date: ")
    days_date = datetime.strftime(today, "%d-%m-%y")
    weekdays = {1: "Monday",
                2: "Tuesday",
                3: "Wednesday",
                4: "Thursday",
                5: "Friday",
                6: "Saturday",
                7: "Sunday"}
    day = weekdays[today.isoweekday()]
    month = today.month
    day_no = today.day
    st.markdown(f"#### Date: {days_date}")
    st.write(f"Day: {day}")
    days_points = st.text_area(label="Today's Challenge",
                               value="Update your challenge here")
    days_list = [pt for pt in days_points.split('\n')]
    submit = st.button("submit")
    if submit:
        todays_data = {
            "date": days_date,
            "day": day,
            "points": days_list
        }
        try:
            data.append(todays_data)
            st.write(len(data))
            with open(file_json, 'w') as updt:
                json.dump(data, updt)
        except Exception as e:
            data = [todays_data]
            with open(file_json, 'w') as updt:
                json.dump(data, updt)
            print(e)
        st.rerun()

    with open(file_json, 'r') as out:
        st.download_button(label="SaveProgress",
                           data=out,
                           mime="application/json",
                           file_name=f"progress_till_{day_no}_{month}.json")
