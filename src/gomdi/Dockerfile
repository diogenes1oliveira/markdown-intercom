# Build Stage
FROM golang:1.22 AS build-stage

WORKDIR /app
ADD . /app

RUN make build-alpine

# Final Stage
FROM alpine:latest

WORKDIR /app

COPY --from=build-stage /app/bin/mdintercom /app/mdintercom
RUN chmod +x /app/mdintercom

# Create appuser
RUN adduser -D -g '' mdintercom
USER mdintercom

CMD ["/app/mdintercom"]
