import json
import socket
import ssl

host_addr = 'api.vk.com'
port = 443


def request(socket, request):
    socket.send((request + '\n' * 2).encode())
    recv_data = socket.recv(65535).decode("windows-1251")
    return recv_data


def get_inf(name, token):
    query = f"user_ids={name}&" + \
            "fields=city,bdate,counters&" + \
            f"access_token={token}&" + \
            "v=5.131"

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect((host_addr, port))
        client = ssl.wrap_socket(client)
        response = request(client, f'GET /method/users.get?{query} HTTP/1.1\nHost: {host_addr}')
    return json.loads(response.split("\n")[-1])


def handle_response(response):
    result = "Информация о пользователе: \n"
    result += "----------------------------------- \n"
    result += "ID пользователя: " + str(response["response"][0]["id"]) + "\n"
    result += "Имя: " + str(response["response"][0]["first_name"]) + "\n"
    result += "Фамилия: " + str(response["response"][0]["last_name"]) + "\n"
    result += "Город: " + response["response"][0]["city"]["title"] + "\n"
    result += "Количество видео: " + str(response["response"][0]["counters"]["videos"]) + "\n"
    result += "Количество аудио: " + str(response["response"][0]["counters"]["audios"]) + "\n"
    result += "Количество подарков: " + str(response["response"][0]["counters"]["gifts"]) + "\n"
    result += "Количество подписок: " + str(response["response"][0]["counters"]["subscriptions"]) + "\n"
    result += "Количество альбомов: " + str(response["response"][0]["counters"]["albums"]) + "\n"
    result += "Количество фотографий: " + str(response["response"][0]["counters"]["photos"]) + "\n"
    result += "Количество подписчиков: " + str(response["response"][0]["counters"]["followers"]) + "\n"
    result += "----------------------------------- \n"
    return result


if __name__ == '__main__':
    id, token = input("Enter id and token: id,token\n").split(',')
    response = get_inf(id, token)
    result = handle_response(response)
    print("\n" + result)
