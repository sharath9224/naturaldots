from fastapi import FastAPI, HTTPException, Query
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
import psycopg2
from psycopg2.extras import RealDictCursor

app = FastAPI()

# Database connection parameters
DB_CONFIG = {
    'dbname': 'sharath',
    'user': 'postgres',
    'password': 'Sharath@9224',
    'host': 'localhost',
    'port': '5433',
}

# Function to establish a connection to PostgreSQL
def connect_to_postgres():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        print("Connected to PostgreSQL database")
        return conn
    except Exception as e:
        print("Error while connecting to PostgreSQL database:", e)
        return None

# Function to get a cursor for executing queries
def get_cursor():
    conn = connect_to_postgres()
    if conn:
        return conn.cursor(cursor_factory=RealDictCursor)
    else:
        return None

# Pydantic models
class Location(BaseModel):
    latitude: float
    longitude: float

class Parameters(BaseModel):
    id: Optional[int] =None
    pH: Optional[float] = None
    conductivity: Optional[float] = None
    DO: Optional[float] = None
    contaminants: Optional[List[str]] = None

class Observation(BaseModel):
    #location: Location
    location: Location
    date_time: datetime
    description: str
    parameters: Parameters

# CRUD operations
@app.post("/observations/", response_model=Observation)
async def create_observation(observation: Observation):
    cursor = get_cursor()
    if cursor:
        try:
            query = """
                INSERT INTO observations (id, date_time, description, pH, conductivity, DO, contaminants,latitude, longitude)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s,%s)
                RETURNING *
            """
            params = (
                observation.id,
                observation.location.latitude,
                observation.location.longitude,
                observation.date_time,
                observation.description,
                observation.parameters.pH,
                observation.parameters.conductivity,
                observation.parameters.DO,
                observation.parameters.contaminants,
            )
            cursor.execute(query, params)
            result = cursor.fetchone()
            return result
        except Exception as e:
            print("Error creating observation:", e)
            raise HTTPException(status_code=500, detail="Error creating observation")
        finally:
            cursor.close()
    else:
        raise HTTPException(status_code=500, detail="Database connection error")

@app.get("/observations/", response_model=List[Observation])
def read_observations(latitude: Optional[float] = None, longitude: Optional[float] = None, start_date: Optional[datetime] = None, end_date: Optional[datetime] = None, pH: Optional[float] = None, conductivity: Optional[float] = None, DO: Optional[float] = None, contaminants: Optional[List[str]] = Query(None)):
    cursor = get_cursor()
    if cursor:
        try:
            conditions = []
            params = []
            if id:
                conditions.append("id = %s")
                params.extend([id])
            if latitude and longitude:
                conditions.append("(latitude = %s AND longitude = %s)")
                params.extend([latitude, longitude])
            if start_date and end_date:
                conditions.append("(date_time)")
                params.extend([date_time])
            if pH:
                conditions.append("pH = %s")
                params.append(pH)
            if conductivity:
                conditions.append("conductivity = %s")
                params.append(conductivity)
            if DO:
                conditions.append("DO = %s")
                params.append(DO)
            if contaminants:
                conditions.append("contaminants @> %s")
                params.append(contaminants)

            conditions_str = " AND ".join(conditions)
            query = "SELECT * FROM observations WHERE " + conditions_str
            cursor.execute(query, params)
            results = cursor.fetchall()
            return results
        except Exception as e:
            print("Error reading observations:", e)
            raise HTTPException(status_code=500, detail="Error reading observations")
        finally:
            cursor.close()
    else:
        raise HTTPException(status_code=500, detail="Database connection error")


"""@app.update("/observations/", status_code=204)
async def update_observations(data: ObservationCreate):
    Update an observation in the database
    with connect_db() as db:
        cursor = db.cursor()
        try:
            # Check that required fields are present
            assert data.station is not None
            assert data.date_time is not None

            # Convert date from string to datetime object
            data.date_time = datetime.datetime.fromisoformat(data.date_time).replace(tzinfo=datetime.timezone.utc)
            data.date_time = datetime.datetime.fromisoformat(data.date_time).replace(tzinfo=datetime.timezone.utc)      
            data.date_time = datetime.datetime.fromisoformat(data.date_time)
            
            # Insert new row or update existing row
            query = (
                "INSERT INTO observations ("
                "station, date_time, depth, temperature,"
                "salinity, conductivity, DO, contaminants)"
                "VALUES(%s, %s, %s, %s, %s,  %s, %s, %s, %s)"
                "ON CONFLICT (station, date_time) DO UPDATE SET"
                "(depth = EXCLUDED.depth,"
                "temperature = EXCLUDED.temperature,"
                "salinity = EXCLUDED.salinity,"
                "conductivity = EXCLUDED.conductivity,"
                "DO = EXCLUDED  .DO,"
                "contaminants = EXCLU   DED.contaminants;"
            )
            cursor.execute(query, (
                data.station,
                data.date_time,
                data.depth,
                data.temperature,
                data.salinity,
                data.conductivity,
                data.DO,        
                json.dumps(data.contaminants),
            ))

            # Commit changes and close connection
            db.commit()
            return Response("", status_code=204)

        except AssertionError as e:
            return Response(f"Missing field in request body: {e}", status_code=400)
        except Exception as e:
            db.rollback()
            print(traceback.print_exc())
            return Response(str(e), status_code=500)
    #else:
        return Response("Method not allowed.", status_code=405)             """

            
if  __name__ == '__main__':
    uvicorn.run('server:app', host='127.0.0.1', port=8000, log_level='info')
