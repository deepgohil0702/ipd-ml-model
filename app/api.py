import pickle
from fastapi import FastAPI

app = FastAPI()

with open('app/gasleakage.pkl', 'rb') as f:
    model = pickle.load(f)


@app.get("/predict-leakage", tags=["Root"])
async def predict(temperature: float, humidity: float, lpg: float):

    new_temperature = int(temperature + (0.5 if temperature >= 0 else -0.5))
    new_humidity = int(humidity + (0.5 if humidity >= 0 else -0.5))
    new_lpg = ((lpg - 0.1) * (0.016567 - 0.002693) / (10 - 0.1)) + 0.002693 

    print(new_temperature)
    print(new_humidity)
    print(new_lpg)

    new_data_point = [[new_humidity, new_lpg, new_temperature]]
    predicted_cluster = model.predict(new_data_point)
    print(predicted_cluster[0])

    is_leakage = False
    if predicted_cluster[0] == 1:
        if (new_temperature >= 25 and new_temperature <= 30) and (new_humidity >= 40 and new_humidity <= 52) and (new_lpg >= 0.004654):
            print("Cluster 1.1")
            is_leakage = True
        elif (new_temperature >= 18 and new_temperature <= 24) and (new_humidity >= 40 and new_humidity <= 57) and (new_lpg >= 0.004374):
            print("Cluster 1.2")
            is_leakage = True
        elif (new_temperature >= 6 and new_temperature < 18) and (new_lpg >= 0.003954):
            print("Cluster 1.3")
            is_leakage = True
        elif (new_temperature < 6) and (new_lpg >= 0.003954):
            print("Cluster 1.4")
            is_leakage = True
        else:
            print("Cluster 1.5")
            if (new_lpg >= 0.004654):
                print("Cluster 1.5.1")
                is_leakage = True
    elif predicted_cluster[0] == 2:
        if (new_temperature >= 25 and new_temperature <= 30) and (new_humidity >= 52 and new_humidity <= 60) and (new_lpg >= 0.004654):
            print("Cluster 2.1")
            is_leakage = True
        elif (new_temperature >= 18 and new_temperature <= 24) and (new_humidity > 52 and new_humidity <= 60) and (new_lpg >= 0.004374):
            print("Cluster 2.2")
            is_leakage = True
        elif (new_temperature < 18) and (new_humidity > 52 and new_humidity <= 60) and (new_lpg >= 0.003954):
            print("Cluster 2.3")
            is_leakage = True
        elif (new_temperature >= 18 and new_temperature <= 24) and (new_humidity > 60 and new_humidity <= 75) and (new_lpg >= 0.004935):
            print("Cluster 2.4")
            is_leakage = True
        elif (new_temperature >= 18 and new_temperature <= 24) and (new_humidity > 75) and (new_lpg >= 0.005355):
            print("Cluster 2.5")
            is_leakage = True
        elif (new_temperature < 18) and (new_humidity > 60 and new_humidity <= 75) and (new_lpg >= 0.004935):
            print("Cluster 2.6")
            is_leakage = True
        elif (new_temperature < 18) and (new_humidity > 75) and (new_lpg >= 0.005355):
            print("Cluster 2.7")
            is_leakage = True
        else:
            print("Cluster 2.8")
            if (new_lpg >= 0.005355):
                print("Cluster 2.8.1")
                is_leakage = True
    elif predicted_cluster[0] == 0:
        if (new_humidity >= 60 and new_humidity <= 75) and (new_lpg >= 0.004935):
            print("Cluster 0.1")
            is_leakage = True
        elif (new_humidity > 75) and (new_lpg >= 0.005355):
            print("Cluster 0.2")
            is_leakage = True
        else:
            print("Cluster 0.3")
            if (new_temperature >= 6 and new_temperature <= 18) and (new_lpg >= 0.003954):
                print("Cluster 0.3.1")
                is_leakage = True
            elif (new_temperature < 6) and (new_lpg >= 0.003673):
                print("Cluster 0.3.2")
                is_leakage = True
    else:
        print("Cluster 4")
        is_leakage = False
    response = {'leakage': 'yes' if is_leakage else 'no'}
    return response


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)