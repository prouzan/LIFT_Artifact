#include <stdio.h>

int main() {
    int id, maxId, tmp;
    scanf("%d%d", &id, &maxId);
    printf("[Testing] <Interface V4.0> (Log all variables for reuse)\n");

    if(0 <= id && id < maxId) {
        tmp = id+1;
        while(tmp!=id) {
            printf("id:%d,maxId:%d,tmp:%d\n", id, maxId, tmp);
            if (tmp <= maxId) {
                tmp = tmp + 1;
            } else {
                tmp = -tmp;
            }
        }
    }

    return 0;
}
