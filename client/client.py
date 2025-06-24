import socket
import time

def main():
    host = '127.0.0.1'  # 서버와 같은 컴퓨터일 경우 localhost
    port = 4000

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))

    print("MUD 서버에 접속했습니다.\n")

    while True:
        try:
            data = sock.recv(2048)
            if not data:
                print("서버 연결이 종료되었습니다.")
                break
            print(data.decode('cp949', errors='ignore'), end='')
        except Exception as e:
            print(f"수신 오류: {e}")
            break

        try:
            print("입력 대기 중...")
            msg = input()
        except EOFError:
            print("입력 스트림이 닫혔습니다.")
            break

        if not msg:
            print("입력이 비어있습니다.")
        sock.sendall(msg.encode('cp949'))

        if msg.lower() in ('exit', 'quit', '끝'):
            break

    sock.close()
    print("클라이언트 종료")

if __name__ == '__main__':
    main()
