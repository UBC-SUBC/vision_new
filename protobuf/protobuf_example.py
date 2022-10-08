import generated.VisionDAQ_pb2 as messaging

if __name__ == '__main__':
    message = messaging.FromDAQ()
    message.yaw = 5
    message.pitch = 1
    message.rpm = 1
    message.depth = 1
    message.speed = 1
    message.battery = True
    
    print('Input object:\n', message)

    message = message.SerializeToString()
    print('Encoded object:\n', message)

    new_message = messaging.FromDAQ()
    new_message.ParseFromString(message)
    print('\nDecoded object:\n', new_message)

    print('It\'s the same UwU, how fantastic!')
