import data_stimu
import time

from iotc import IOTCConnectType, IoTCClient, IOTCEvents

from weatherapi import get_weather

# Replace these values
ID_SCOPE = "0ne00B88AA2"
DEVICE_ID = "352qadk8w"
ACCESS_KEY = "nZdqVOEjtkWK4vap1CGVNZLk4Wbjl/o8ida3AyHHs6k="
WATERING = 0
WATERING_COUNT = 0
STOP_WATERING = False
START_WATERING = False
SYS_STATE = 0
LAT = 1.291390
LON = 103.857269


def on_commands(command):
    global WATERING, STOP_WATERING, START_WATERING, SYS_STATE
    cmd_name = command.name
    # cmd_value = command.value
    if cmd_name == "ForceWatering":
        WATERING = 1
        STOP_WATERING = True
        SYS_STATE = 1
        print("Received command \"Force Watering\"!\n")
    elif cmd_name == "ForceStopWatering":
        WATERING = 0
        START_WATERING = True
        SYS_STATE = 2
        print("Received command \"Force Stop Watering\"!\n")
    elif cmd_name == "ResetAction":
        START_WATERING = STOP_WATERING = False
        WATERING = 0
        SYS_STATE = 0
        print("Received request to reset system feature!\n")
    command.reply()


def main():
    global WATERING, WATERING_COUNT, SYS_STATE
    device = IoTCClient(DEVICE_ID, ID_SCOPE,
                        IOTCConnectType.IOTC_CONNECT_DEVICE_KEY, ACCESS_KEY)
    device.on(IOTCEvents.IOTC_COMMAND, on_commands)

    try:
        device.connect()
        print("Device connected")
        while True:

            stim_moisture, stim_temperature = data_stimu.data_stimulation(WATERING)
            current_condition, fore_condition, fore_raining, fore_precip_mm = get_weather(LAT, LON)

            if WATERING == 1 and WATERING_COUNT < 2:
                WATERING_COUNT += 1

            if not (STOP_WATERING and START_WATERING):
                if stim_moisture < 30 and 20 < stim_temperature < 30 and WATERING == 0 and fore_precip_mm <= 2:
                    WATERING = 1
                elif stim_moisture > 50 and WATERING == 1:
                    WATERING = 0
                    WATERING_COUNT = 0

            flow_rate = {0: 0, 1: 0.5, 2: 2.5}
            stim_flow = flow_rate[WATERING_COUNT]

            if 0 < fore_precip_mm <= 2:
                raining_amount = 1
            elif 2 < fore_precip_mm < 5:
                raining_amount = 2
            elif fore_precip_mm >= 5:
                raining_amount = 3
            else:
                raining_amount = 0

            telemetry_data = {
                # "_eventcreationtime": datetime.utcnow().isoformat()[:-3]+"Z",
                "SoilMoisture": stim_moisture,
                "AirTemperature": stim_temperature,
                "WaterFlow": stim_flow,
                "CurrentlyWatering": WATERING,
                "SystemState": SYS_STATE,
                "CurrentWeather": current_condition,
                "Raining": fore_raining,
                "RainingAmount": raining_amount,
                "WeatherCondition": fore_condition
            }

            """if stim_moisture < 0:
                print(count)
                break
            count+=1"""

            # print(telemetry_data)
            device.send_telemetry(telemetry_data)
            # print(f"Sent telemetry data: {telemetry_data}")

            time.sleep(5)

    except Exception as e:
        print(f"{e}")


# Run the asynchronous coroutine
if __name__ == "__main__":
    main()
