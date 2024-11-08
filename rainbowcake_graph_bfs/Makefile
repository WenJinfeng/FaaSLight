SHELL := /bin/bash

# Default configurations
LAMBDA_NAME ?= rainbowcake_graph_bfs
S3_BUCKET ?= ssmtariq-general
ZIP_FILE_NAME ?= rainbowcake_graph_bfs.zip
PYTHON_VERSION ?= 3.9
HANDLER ?= handler.handler
TIMEOUT ?= 60
MEMORY_SIZE ?= 1024
RUNTIME ?= python$(PYTHON_VERSION)
ENV_VARS ?= "Variables={PYTHONPROFILEIMPORTTIME=1,EXAMPLE_VAR=EXAMPLE_VAL}"
PACKAGE_DIRNAME ?= "package"
ROLE_ARN ?= "arn:aws:iam::679551966535:role/sebs-lambda-role"
API_URL = "https://syxhpt4fdgv6cpw4zaxkrpcxzi0wvduj.lambda-url.us-east-2.on.aws/"
INVOKE_COUNT ?= 1
AWS_REGION = us-east-2

install:
	@echo "Building the lambda package..."
	rm -rf $(PACKAGE_DIRNAME)
	mkdir $(PACKAGE_DIRNAME)
	pip install -r ./requirements.txt --platform manylinux2014_x86_64 --target=./$(PACKAGE_DIRNAME) --implementation cp --python-version $(PYTHON_VERSION) --only-binary=:all: --upgrade

# make strip-package PACKAGE_DIRNAME=package_before
strip-package:
	@echo "Stripping unneeded files in pack..."
	cd $(PACKAGE_DIRNAME) && \
	rm -rf setuptools* wheel* pip* pkg* && \
	find . -type d -name "tests" -exec rm -rf {} + && \
	find . -name "*.so" | xargs strip && \
	find . -name "*.so.*" | xargs strip && \
	find . -name "*.pyc" -delete

pack:
	@echo "Updating the lambda package build..."
	rm -rf $(ZIP_FILE_NAME)
	cd $(PACKAGE_DIRNAME); zip -r ../$(ZIP_FILE_NAME) .; cd ..
	zip -r $(ZIP_FILE_NAME) handler.py

add-profiler:
	@echo "Updating the lambda package build to include profiler..."
	ln -s ../../profiler ./profiler
	zip -r $(ZIP_FILE_NAME) profiler

# Create the lambda function on AWS (only to be used once to create the function)
create-function:
	@echo "Creating Lambda function on AWS..."
	aws lambda create-function --function-name $(LAMBDA_NAME) \
	--runtime $(RUNTIME) --role $(ROLE_ARN) --handler $(HANDLER) \
	--zip-file fileb://$(ZIP_FILE_NAME) --timeout $(TIMEOUT) --memory-size $(MEMORY_SIZE) \
	--environment $(ENV_VARS) --region $(AWS_REGION)

# Update the lambda function code on AWS
upload-code:
	@echo "Uploading code to S3..."
	aws s3 cp $(ZIP_FILE_NAME) s3://$(S3_BUCKET)/$(ZIP_FILE_NAME)

# Update the lambda function code on AWS
update-code:
	@echo "Updating Lambda function code on AWS..."
	aws lambda update-function-code --function-name $(LAMBDA_NAME) --s3-bucket $(S3_BUCKET) --s3-key $(ZIP_FILE_NAME)

# Update the lambda function configuration on AWS
update-configuration:
	@echo "Updating Lambda function configuration on AWS..."
	aws lambda update-function-configuration --function-name $(LAMBDA_NAME) \
	--handler $(HANDLER) --timeout $(TIMEOUT) --memory-size $(MEMORY_SIZE) \
	--runtime $(RUNTIME) --environment $(ENV_VARS)

# Invoke the lambda function in parallel, this is useful because all concurrent invocations will be cold start
invoke-par:
	@echo "Invoking in parallel..."
	@for i in {1..$(INVOKE_COUNT)}; do \
		curl --request POST \
			--url $(API_URL) \
			--header 'Content-Type: application/json' & \
	done; wait

# Invoke the lambda function sequentially
invoke-seq:
	@echo "Invoking sequentially..."
	@for i in {1..$(INVOKE_COUNT)}; do \
		echo $$i; \
		curl --request POST \
			--url $(API_URL) \
			--header 'Content-Type: application/json'; \
		echo ""; \
	done

# Optimize the lambda package
optimize:
	@echo "Optimizing the lambda package..."
	diff -x "*.pyc" -bur package_before $(PACKAGE_DIRNAME) --color

# Default target
all: deploy

.PHONY: build deploy invoke-parallel invoke-sequential optimize clean all