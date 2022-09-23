
import toml

def main():
    camera_settings = toml.load("CameraSettings.toml")

    print(camera_settings["camera1"]["address"])

    for camera_name,camera in camera_settings.items():
        pass
if __name__ == '__main__':
    main()





