
set -exo pipefail

if [ ! -d "stubs" ]; then
  mkdir -p "stubs"
else
  rm -rf ./stubs/*pb2*.py
fi
touch stubs/__init__.py
cd ./protos

python -m grpc_tools.protoc \
        -I ./ \
        --python_out=../ \
        --grpc_python_out=../ \
        stubs/*.proto

cd ..

mkdir -p ./second_service/stubs
mkdir -p ./first_service/stubs

rm -rf ./second_service/stubs/*_pb2*.py
rm -rf ./first_service/stubs/*_pb2*.py


touch ./second_service/stubs/__init__.py
touch ./first_service/stubs/__init__.py


cp -r ./stubs/*.py ./second_service/stubs
cp -r ./stubs/*.py ./first_service/stubs

