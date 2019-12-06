# Milestone 2 and 3 Reflection

### Background

Our team sought out to create a dashboard that could help explore the following research questions:

> 1. How has the life expectancy by country changed over time?
> 2. How are monetary factors associated with life expectancy?
> 3. Does the life expectancy between developing and developed countries differ?

We believe that in one week we were able to produce a useful dashboard that can help researchers answer the question above. Through the use of four interactive plots users are able to answer the research questions from a variety of angles.

To improve the dashboard we sought feedback from peers and teaching assistants. Below we have summarized what the app does well, what the current limitations are, and ideas for future improvements.

### What the app does well

- The design is clean and visually appealing. By organizing the plots into columns and the use of *pretty containers* (the 3d box effect) each section clearly stands out and attracts the users eyes to the important sections.
- The interactivity of the dashboard allows for the dashboard to remain minimal, while providing detailed numbers when required. For example:
  - The heat map is not crowded with labels making it nice to look at. If you need to know the name of a country or exact value you can hover the mouse over a country to get the details.
  - The line plots also take a minimalist approach. To see detailed precise numbers the user can hover the cursor over any year to see the values for those years.

### Current limitations

- The design proposal was ambitious given the time constraints. We were not able to create all the features we had originally proposed:
  - No histogram for life expectancy was created.
  - The line plots do have the functionality to change what the colour of the line represents.
- There are over 193 countries. There is the possability for a user to select all 193 countries if they wish. This results in overplotting and reduces the usefullness of the plot.
  - ![overplotting_example](../assets/overplotting_example.png)
- Upon reviewing the data in detail there appear to be issues with data quality. Some of these issues were also noted on the [Kaggle page](https://www.kaggle.com/kumarajarshi/life-expectancy-who/data) where the data was obtained:
  - Canada and Greece are listed as a developing countries.
  - There is no GDP data for the USA.
  - `percentage expenditure` has some values which are greater than 100 (it is mean to represent the percent of GDP spent on health).

### Feedback and Ideas for future improvement

Based on self reflection, discussions with our peers, and feedback from TAs we have identified several areas of improvement. Due to limited time constraints not all of these items have been implemented. Below is a summary of feedback and an explanation of what has beeen implemented to date.

#### Layout

| Feedback                                                     | Status                                                       |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| The plots can be cut-off and not look correct on certain size screens ([#41](https://github.com/UBC-MDS/DSCI_532_L01_group101_dashboards/issues/41), [#39](https://github.com/UBC-MDS/DSCI_532_L01_group101_dashboards/issues/39)) | *To do - High Priority:* The development team is experimenting with the use of the grid system from the [bootstrap documentation](https://getbootstrap.com/docs/4.0/layout/grid/). However this issue will likely persist when creating the plots with Altair as they must be embed into an HTML iFrame which is a fixed size. |
| Title text size is small. Readability could be improved by increasing size. ([#42](https://github.com/UBC-MDS/DSCI_532_L01_group101_dashboards/issues/42)) | *Complete:* This update was made as the level of effort was low and improved the visual appearence of the app ([PR #45](https://github.com/UBC-MDS/DSCI_532_L01_group101_dashboards/pull/45)) |
| The control buttons are not obvious when you load the app because they  are at the bottom of the page. Could look better to move to the top  ([#42](https://github.com/UBC-MDS/DSCI_532_L01_group101_dashboards/issues/42)) | *Complete:* The development team agreed with users that the current placement of the filters was confusing. The layout was improved by moving filters above the plots they control ([PR #45](https://github.com/UBC-MDS/DSCI_532_L01_group101_dashboards/pull/45)) |
| It is not clear what the filters on the left control. Move these filters to above or on top of the plots they effect ([#43](https://github.com/UBC-MDS/DSCI_532_L01_group101_dashboards/issues/43)) | *Complete:* The development team agreed with users that the current placement of the filters was confusing. The layout was improved by moving filters above the plots they control ([PR #45](https://github.com/UBC-MDS/DSCI_532_L01_group101_dashboards/pull/45)) |

#### Summary Statistics

| Feedback                                                     | Status                                                       |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| The summary stats at the top are confusing. Do they change with the filters? ([#42](https://github.com/UBC-MDS/DSCI_532_L01_group101_dashboards/issues/42), [#39](https://github.com/UBC-MDS/DSCI_532_L01_group101_dashboards/issues/39)) | *Complete:*  By moving all filters to be position above the plots they control should clarify that the summary statistics do not change with the filters ([PR #45](https://github.com/UBC-MDS/DSCI_532_L01_group101_dashboards/pull/45)). This has also been documented in the project README ([PR #46](https://github.com/UBC-MDS/DSCI_532_L01_group101_dashboards/pull/46)). |
| It is confusing to have the decription of the summary statistic below the number as opposed to above. ([#42](https://github.com/UBC-MDS/DSCI_532_L01_group101_dashboards/issues/42)) | *Complete:* This was corrected as it was a very quick fix to implement ([PR #45](https://github.com/UBC-MDS/DSCI_532_L01_group101_dashboards/pull/45)) |

#### Line plot

| Feedback                                                     | Status                                                       |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| Add in a control to limit the number of countries that can be drawn on line plot. | *To do - Low Priority:* This was deemed to be a low priority control as it is unlikely the user will create a view with overplotting. To do so they would have to select many countries from the dropdown menu. This issue should be corrected eventually moving forward to ensure app quality. |
| It is not clear why Mexico and Turkey are the defaults when the app loads. Additionally they do not appear in the drop-down list when the app loads. ([#43](https://github.com/UBC-MDS/DSCI_532_L01_group101_dashboards/issues/43)) | *Complete:* Through user testing this bug was dicovered. The developers have updated the app to ensure that the countries appearing on the line plot also show on the drop down menu ([PR #45](https://github.com/UBC-MDS/DSCI_532_L01_group101_dashboards/pull/45)). Additionally it was decided that Germany, Italy, and Spain would be the three default countries as these are prominent well known countries. However this could be customized for future users based on their needs ([PR #45](https://github.com/UBC-MDS/DSCI_532_L01_group101_dashboards/pull/45)). |
| Limit the domain on the y-axis to reasonable values (e.g. life expectancy does not need to show 0) ([#43](https://github.com/UBC-MDS/DSCI_532_L01_group101_dashboards/issues/43)) | *To do - High Priority:* The developers agree this is an important update to make sure the plots are not misleading in any way. This change has not yet been implemented due to time constraints. |

#### Map

| Feedback                                                     | Status                                                       |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| For values that are null or not existing the country should be shaded grey ([#43](https://github.com/UBC-MDS/DSCI_532_L01_group101_dashboards/issues/43)). | *To do - high priority:* The developers agree with the user feedback. The dashboard will look better if missing countries were shaded grey as oppposed to white on the map. This should be updated as soon as possible to increase the quality of the app. |
| Map each country to a region or continent. This could enable for comparisons by region / continent as opposed to just country by country. It would also allow users to compare a countries performance relative to the continental/regional mean. | *To do - low priority:* This feature will increase the usefullness of the dashboard for users but is not necessary. |

#### Line plot

| Feedback                                                     | Status                                                       |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| For the “point colour” part in the scatterplot, it would be interesting  to have the option to only show developed vs. undeveloped countries  rather than both at the same time ([#39](https://github.com/UBC-MDS/DSCI_532_L01_group101_dashboards/issues/39)). | *To do - low priority:* This feature will increase the usefullness of the dashboard for users but is not necessary. |

#### Other

| Feedback                                                     | Status                                                       |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| Obtain correct or more accurate GDP and life expectancy data. | *To do - high priority:* This change has not yet been implented as the developers are actively creating an R based version of the dashboard as well. To ensure continuity between the two apps these updates can be made after the R dashboard is complete. This is high priority as some of the results may be incorrect or misleading, jeaprodizing the usefullness of the app. |
| Add in the ability to quickly create interesting views. For example, develop a button that can quick filter to top 10 worst or best performing countries. | *To do - low priority:* This feature will increase the usefullness of the dashboard for users but is not necessary. |

### Reflection on Usefullness of Feedback

The development team found the experience of sitting with users and obtaining feedback in person very valuable. At times it was frustrating to watch the user "*use the dashboard incorrectly*". But the experience was more so eye opening to see how a fresh pair of eyes interacts with the dashboard.

There were two main themes that came out during the feedback session:

1. Issues with layout (user needed to scroll to see full plot)
2. Confusion on which interactions control which plots

As a developer it is easy to forget that what is obvious to you may not be obvious to your user. A few points of feedback may have been opinionated, but the developer team believes the vast majority of feedback was very valuable and should be actioned.

Moving forward user testing will continue to be an important part of the development process. If the user is not happy, the development team is not happy!