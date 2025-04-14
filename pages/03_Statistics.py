import streamlit as st
import pandas as pd 
import plotly.express as px
import time
import numpy as np
import plotly.graph_objects as go
from datetime import datetime, timedelta


st.set_page_config(page_title="Statistics", page_icon="📊")

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if st.session_state["logged_in"]:
    with st.spinner("Statistic data is loading", show_time=True):
        statistics = pd.read_pickle("statistic_data/user.pkl")

        #Add a progress bar
        total_words = len(st.session_state.dictionary)
        learned_words = st.session_state.dictionary["learned"].sum()
        learned_ratio = learned_words / total_words if total_words > 0 else 0

        # Display learned words ratio in text form
        st.metric(label="Learned Words Ratio", value=f"{learned_words}/{total_words} ({learned_ratio*100:.1f}%)")

        # Display progress bar
        st.progress(learned_ratio)  # This will show the ratio as a progress bar (0 to 100%)

        # Convert date column to datetime format
        statistics["date"] = pd.to_datetime(statistics["date"], format="%d/%m/%Y")

        # Count total attempts per date
        total_counts = statistics["date"].value_counts().reset_index()
        total_counts.columns = ["date", "Words trained"]
        total_counts = total_counts.sort_values("date")

        # Count mistakes (where success == False)
        mistake_counts = statistics[statistics["success"] == False]["date"].value_counts().reset_index()
        mistake_counts.columns = ["date", "Mistakes"]
        mistake_counts = mistake_counts.sort_values("date")

        # Merge both counts into one DataFrame
        combined_counts = total_counts.merge(mistake_counts, on="date", how="left").fillna(0)
        combined_counts["Mistakes"] = combined_counts["Mistakes"].astype(int)  # Ensure integer values

        # Melt the DataFrame for grouped bar plotting
        #combined_counts = combined_counts.melt(id_vars=["date"], var_name="Category", value_name="Count")

        #Create statistics for the learned words
        learned =  statistics[statistics["learned"] == 1].groupby("date").size().reset_index(name="learned_count")

        fig = go.Figure()

        # Create a grouped bar chart
        fig.add_trace(go.Bar(
            x = combined_counts["date"],
            y = combined_counts["Words trained"],
            name='Trained words',
            #marker=dict(
            #    color=combined_counts["Words trained"],        # Assign bar heights as color values
            #    colorscale='Sunset',  # Color scale for bars
            #    showscale=False      # Show colorbar
            #  )
        ))
        fig.add_trace(go.Bar(
            x = combined_counts["date"],
            y = combined_counts["Mistakes"],
            name="Mistakes",
            #marker=dict(
            #    color=combined_counts["Words trained"],        # Assign bar heights as color values
            #    colorscale='Sunset',  # Color scale for bars
            #    showscale=False      # Show colorbar
            #  )
        ))

        fig.add_trace(go.Scatter(
              x=learned["date"],
              y=learned["learned_count"],
              name="Learned words",
            #  line=dict(
            #    color='red',      # Change line color
            #    width=1          # Change line width
            #  ),
              marker=dict(
                size=8,           # Change marker size
                symbol='circle'   # Marker style (e.g., 'square', 'diamond', 'cross', etc.)
              )
              ))
        #fig = px.bar(combined_counts, x="date", y="Count", color="Category",
        #            title="Total words trained per day",
        #            labels={"date": "Day", "Count": "", "Category": "Type"},
        #            barmode="group",
        #            color_discrete_sequence=px.colors.sequential.Sunsetdark)  # 'group' ensures side-by-side bars

        # Customize layout
        fig.update_layout(
            xaxis=dict(
                showgrid=False,
                tickformat="%d-%m",
                nticks=3  # Limit to 3 x-axis ticks
            ),
            yaxis=dict(showgrid=True,
                       gridcolor="lightgray",
                       nticks=4),
            barmode="overlay",
        )
        
        st.plotly_chart(fig)


        # Convert the 'date_added' column to datetime format
        dictionary = st.session_state.dictionary.copy()
        dictionary["date_added"] = pd.to_datetime(dictionary["date_added"], format="%d/%m/%Y")

        # Extract month and year
        dictionary["month_year"] = dictionary["date_added"].dt.to_period("M").astype(str)

        # Count how many words were added each month
        monthly_word_count = dictionary.groupby("month_year").size().reset_index(name="words_added")

        # Create a bar chart using Plotly
        fig2 = px.bar(
            monthly_word_count,
            x="month_year",
            y="words_added",
            title="Words Added to Dictionary by Month",
            labels={"month_year": "Month", "words_added": "Number of Words Added"},
            color="words_added",  # Color the bars based on the number of words added
            color_continuous_scale="Sunsetdark"  # Color scheme for the bars
        )

        # Calculate start and end of x-axis range
        today = datetime.today()
        start_date = datetime(today.year-1, today.month, 1)
        end_date = datetime(today.year, today.month, 1)
        fig2.update_layout(xaxis_range=[start_date, end_date])

        st.plotly_chart(fig2)


        # Compute success ratio and plot the dictionary heat map
        #Add empty words to fit the 
        num_cols = 7
        num_empty_words = num_cols - len(dictionary)%num_cols
        num_rows = int((len(dictionary)+num_empty_words)/num_cols)
        

        # Define a pastel green-to-red colorscale
        custom_colorscale = [
            [0.0, "rgb(255, 182, 193)"],  # Pastel Red (Low values)
            [1.0, "rgb(153, 255, 187)"]   # Pastel Green (High values)
        ]


        dictionary["success ratio"] = dictionary["num_success"] / dictionary["num_practiced"]
        dictionary.loc[dictionary["learned"] == True, "success ratio"] = 1  # If learned, set ratio to 1

        # Sort words by success ratio (highest to lowest)
        dictionary = dictionary.sort_values(by="success ratio", ascending=False).reset_index(drop=True)

        #Add empty words at the beginning
        empty_rows = pd.DataFrame([[""] * dictionary.shape[1]] * num_empty_words, columns=dictionary.columns)
        dictionary = pd.concat([empty_rows,dictionary], ignore_index=True)

        # Reshape into 5 rows × 4 columns
        heatmap_data = np.array(dictionary["success ratio"]).reshape(num_rows, num_cols)
        word_labels = np.array(dictionary["german"]).reshape(num_rows, num_cols)
        word_labels_eng = np.array(dictionary["english"]).reshape(num_rows, num_cols)

        # Create heatmap without numbers inside
        fig3 = px.imshow(
            heatmap_data,
            color_continuous_scale="Pinkyl",#custom_colorscale,
            aspect = 1.0
        )
        # Add word labels as annotations
        for i in range(num_rows):
            for j in range(num_cols):
                fig3.add_annotation(
                    x=j, y=i,
                    text=word_labels[i, j],  # Only display the word
                    showarrow=False,
                    font=dict(size=14,color="black"),
                    textangle=0,
                    opacity=0.75
                )
        # Customize layout
        fig3.update_layout(
            title="Wrods accuracy ratio",
            xaxis=dict(showticklabels=False, title=""),
            yaxis=dict(showticklabels=False, title=""),
            height = 1000
        )
        fig3.update_coloraxes(showscale=False)
        fig3.update_traces(
                hovertemplate="Word: %{customdata}<br>Success Ratio: %{z:.2f}<extra></extra>",
                customdata=word_labels_eng,  # Attach words for hover display
                xgap = 5,
                ygap = 5
            )
        st.plotly_chart(fig3)

    
    

else: st.write("Please, login")
