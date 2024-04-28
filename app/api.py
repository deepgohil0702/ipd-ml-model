import pickle
from fastapi import FastAPI

app = FastAPI()

with open('app/gasleakage.pkl', 'rb') as f:
    model = pickle.load(f)


@app.get("/", tags=["Root"])
async def predict(temperature: float, humidity: float, lpg: float):

    new_lpg = ((lpg - 0.1) * (0.016567 - 0.002693) / (10 - 0.1)) + 0.002693 

    new_data_point = [[temperature, humidity, new_lpg]]
    predicted_cluster = model.predict(new_data_point)

    is_leakage = False
    if predicted_cluster[0] == 1:
        if (new_lpg >= 0.003954):
            is_leakage = True 
    elif predicted_cluster[0] == 2:
        if (temperature >= 25.0 and temperature <= 30.9) and (humidity >= 40.0 and humidity <= 60.9) and (lpg >= 0.003954):
            is_leakage = True
        elif (temperature >= 31.0 and temperature <= 40.9) and (humidity >= 61.0 and humidity <= 65.9) and (lpg >= 0.004654):
            is_leakage = True
        elif (temperature >= 41.0) and (humidity >= 66.0) and (lpg >= 0.005355):
            is_leakage = True
    else:
        is_leakage = False
    response = {'leakage': 'yes' if is_leakage else 'no'}
    return response
