from server import *


if __name__ == "__main__":
    try: asyncio.run(GameServer().start('127.0.0.1'))
    except KeyboardInterrupt: print("\n[INFO] 서버를 종료합니다.")