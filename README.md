# SQLALCHEMY CHALLENGE

**climate_starter.ipynb**

**1. Precipitation Analysis**
  - Used Python and SQLAlchemy to do a basic climate analysis and data exploration of the climate database.
  - Used the SQLAlchemy create_engine() function to connect to SQLite database.
  - Used the SQLAlchemy automap_base() function to reflect tables into classes, and then save references to the classes named station and measurement.
  - Linked Python to the database by creating a SQLAlchemy session.
  - Performed Precipitation Analysis by:
      - Finding the most recent date in the dataset.
      - Using that date, got the previous 12 months of precipitation data by querying the previous 12 months of data.
      - Loaded the query results into a Pandas DataFrame.
      - Plotted the results by using the DataFrame plot method.
      - Used Pandas to print the summary statistics for the precipitation data.
        
**2. Station Analysis**
  - Designed a query to calculate the total number of stations in the dataset.
  - Designed a query to find the most-active stations (that is, the stations that have the most rows).
  - Listed the stations and observation counts in descending order.
  - Identified station id that has the greatest number of observations - **USC00519281**.
  - Designed a query that calculates the lowest, highest, and average temperatures that filters on the most-active station id found in the previous query.
  - Designed a query to get the previous 12 months of temperature observation (TOBS) data.

**app.py**

- Imported the dependencies.
- Database Setup done using create_engine().
- Reflected an existing database into a new model.
- Reflected the tables.
- Saved references to the tables.
- Defined Flask Routes as follows:
    - "/": Listed all the available routes.
    - "/api/v1.0/precipitation": Converted the query results from precipitation analysis (i.e. retrieve only the last 12 months of data) to a dictionary using date as the key and prcp as the value. Returned the JSON representation of your dictionary.
    - "/api/v1.0/stations": Returned a JSON list of stations and corresponding names from the dataset.
    - "/api/v1.0/tobs": Queried the dates and temperature observations of the most-active station for the previous year of data. Return a JSON list of temperature observations for the previous year.
    - "/api/v1.0/<start>" and "/api/v1.0/<start>/<end>": Returned a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start or start-end range inclusive.
