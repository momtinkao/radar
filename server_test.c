#include <arpa/inet.h>
#include <errno.h>
#include <netdb.h>
#include <netinet/in.h>
#include <stdio.h>
#include <string.h>
#include <sys/socket.h>
#include <unistd.h>

#define BUFFER_SIZE 25600

int main()
{
    int serverlisten_fd;
    int s = -1;
    char _port[6];
    struct addrinfo hints, *servinfo, *p;
    struct sockaddr_in client_addr;
    socklen_t client_len = sizeof(client_addr);
    struct sockaddr_in sin;
    socklen_t len = sizeof(sin);
    char recv_buf[BUFFER_SIZE];
    char send_buf[BUFFER_SIZE];
    int ret;

    snprintf(_port, sizeof(_port), "%d", 10005);
    memset(&hints, 0, sizeof(hints));
    hints.ai_family = AF_INET;
    hints.ai_socktype = SOCK_DGRAM;
    hints.ai_flags = AI_PASSIVE;

    if ((ret = getaddrinfo(NULL, _port, &hints, &servinfo)) != 0)
    {
        fprintf(stderr, "getaddrinfo 錯誤: %s\n", gai_strerror(ret));
        return 1;
    }

    for (p = servinfo; p != NULL; p = p->ai_next)
    {
        if ((s = socket(p->ai_family, p->ai_socktype, p->ai_protocol)) == -1)
        {
            perror("socket 錯誤");
            continue;
        }

        // 設置 SO_REUSEADDR 選項
        int optval = 1;
        if (setsockopt(s, SOL_SOCKET, SO_REUSEADDR, &optval, sizeof(optval)) < 0)
        {
            perror("setsockopt 錯誤");
            close(s);
            continue;
        }

        if (setsockopt(s, SOL_SOCKET, SO_REUSEPORT, &optval, sizeof(optval)) < 0)
        {
            perror("reuse port錯誤");
            close(s);
            continue;
        }

        if (bind(s, p->ai_addr, p->ai_addrlen) < 0)
        {
            perror("bind 錯誤");
            close(s);
            continue;
        }
        break; // 成功綁定
    }

    if (p == NULL)
    {
        fprintf(stderr, "無法綁定套接字\n");
        freeaddrinfo(servinfo);
        return 1;
    }

    serverlisten_fd = s;
    freeaddrinfo(servinfo);

    printf("伺服器正在監聽...\n");

    int recv_bytes = recvfrom(serverlisten_fd, recv_buf, sizeof(recv_buf) - 1, 0, (struct sockaddr *)&client_addr, &client_len);
    int cfd;
    if (recv_bytes > 0)
    {
        int optval = 1;
        cfd = socket(PF_INET, SOCK_DGRAM, 0);
        getsockname(serverlisten_fd, (struct sockaddr *)&sin, &len);
        if (setsockopt(cfd, SOL_SOCKET, SO_REUSEADDR, &optval, sizeof(optval)) < 0)
        {
            perror("new setsockopt錯誤");
            close(cfd);
        }
        if (setsockopt(cfd, SOL_SOCKET, SO_REUSEPORT, &optval, sizeof(optval)) < 0)
        {
            perror("reuse port錯誤");
            close(cfd);
        }
        if (bind(cfd, (struct sockaddr *)&sin, sizeof(struct sockaddr)) < 0)
        {
            perror("new bind錯誤");
        }
        client_addr.sin_family = PF_INET;
        if (connect(cfd, (struct sockaddr *)&client_addr, sizeof(struct sockaddr)) == -1)
        {
            perror("new connect failed");
        }
        recv_buf[recv_bytes] = '\0'; // 為接收到的數據添加空字符結束
        printf("從 %s:%d 接收到 %s\n", inet_ntoa(client_addr.sin_addr), ntohs(client_addr.sin_port), recv_buf);
    }
    else
    {
        perror("recvfrom 失敗");
    }
    while (1)
    {
        memset(send_buf, 0, sizeof(send_buf));
        fgets(send_buf, 25600, stdin);
        memset(recv_buf, 0, sizeof(recv_buf));
        // 發送響應到客戶端
        if (send(cfd, send_buf, sizeof(send_buf), 0) < 0)
        {
            perror("sendto 失敗");
        }
        else
        {
            printf("發送響應成功\n");
        }
        recv_bytes = recv(cfd, recv_buf, sizeof(recv_buf), 0);
        recv_buf[recv_bytes] = '\0';
        printf("recv %s\n", recv_buf);
    }

    close(serverlisten_fd);
    return 0;
}
