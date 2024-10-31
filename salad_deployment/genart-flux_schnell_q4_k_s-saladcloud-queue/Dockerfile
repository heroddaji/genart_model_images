# syntax=docker/dockerfile:1

FROM heroddaji/genart-flux_schnell_q4_k_s-saladcloud:1.0.0

COPY ./salad-http-job-queue-worker-v004 ./
COPY --chmod=755 ./main.sh ./

CMD ["./main.sh"]