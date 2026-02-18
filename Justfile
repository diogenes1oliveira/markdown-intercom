set dotenv-load := true

default:
    just --list

# Run recipes from the Go project (src/gomdi)
go *args:
    cd src/gomdi && just {{args}}
