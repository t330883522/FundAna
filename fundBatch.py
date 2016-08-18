from datetime import datetime

if __name__ == '__main__':
    des_date = datetime.now().replace(hour=14, minute=50, second=0)
    while True:
        print(datetime.now())
        if datetime.now().weekday() in [0, 1, 2, 3, 4] and datetime.now() > des_date:
            pass
