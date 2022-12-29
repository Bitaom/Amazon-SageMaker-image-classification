# Amazon-SageMaker-image-classification
This repository gives detail information on how to build an image classifier using AWS SageMaker.
The codes are written with the Amazon SageMaker Python SDK library. The boto3 library is needed to be installed to integrate with AWS services.
<br/>`pip install boto3`<br/>
## Supported Image Requirements:

  - Maximum file size for an image is 4 MB.
  - Minimum image dimension of an input image file (stored in an Amazon S3 bucket or supplied as image bytes) is 64 pixels x 64 pixels.
  - Maximum image dimension of an input image file (stored in an Amazon S3 or supplied as image bytes) is 4096 pixels x 4096 pixels.
  - Supported file formats are PNG and JPEG image formats.
  - Maximum image aspect ratio is 20:1.
  ## Data gathering and preprocessing

<br/>Part of dataset is passed through the classifier as a training dataset, and the rest is kept as a validation dataset.<br/>

The input of the algorithm is in augmented manifest format, referring to the location of images on the S3 bucket and their labels. The manifest file format is in JSON Lines in which each line represents one sample. SageMaker reads the training and validation data separately from different channels, so the training and validation manifest files are stored on different channels in the same bucket. The algorithm supports image/png, image/jpeg, for inference.

## Image Classification

We use SageMaker image classifier algorithm for this project. The first step is Fine-tuning the Image classification model, and passing the manifest files as the input to the model. The coding for training the classifier is available in [SageMaker\_image\_classification](https://github.com/Bitaom/Amazon-SageMaker-image-classification/blob/main/SageMaker_image_classification.py)

**Training parameters**

There are two kinds of parameters that need to be set for training. The first one is the parameters for the training job, including the &quot;Input specification&quot;, &quot;Output specification&quot;, and &quot;Resource config&quot;. The second group is the hyperparameters that are specific to the algorithm.

<br/>The trained model configuration is saved in the specified path of output, and the specifications of each trained model is observable in the Training section of the SageMaker dashboard.<br/>

<br/>The output of this section is a plot of training and validation accuracy per epoch along with the highest accuracy amount. (The numeric results of training in each epoch are also available through the AWS CloudWatch service).<br/>

## SageMaker Model Creation

After training the model with satisfactory accuracy we need to create a SageMaker Model from the training output. The output of this section is the model ARN which will be used for creating the endpoint ([SageMaker\_model\_creation](https://github.com/Bitaom/Amazon-SageMaker-image-classification/blob/main/SageMaker_model_creation.py).

## Inference

To perform the inference, we first create an endpoint configuration, that describes the distribution of traffic across the models, whether split, shadowed, or sampled in some way. Lastly, we create the endpoint that serves up the model, through specifying the name and configuration defined. The end result is an endpoint that can be validated and incorporated into production application. We can confirm the endpoint configuration and status by navigating to the &quot;Endpoints&quot; tab in the AWS SageMaker console.

<br/>There are two different types of endpoints that can be used for this project: <br/>

**Real-time inference:** Real-time inference is ideal for inference workloads where we have real-time, interactive, low latency requirements.

**Serverless Inference:** Serverless Inference is ideal for workloads which have idle periods between traffic spurts and can tolerate cold starts. Serverless endpoints automatically launch compute resources and scale them in and out depending on traffic, eliminating the need to choose instance types or manage scaling policies.

## Invoke a serverless endpoint

In order to perform inference using a serverless endpoint, we must send an HTTP request to the endpoint. We use the InvokeEndpoint API [Endpoint Invocation](https://github.com/Bitaom/Amazon-SageMaker-image-classification/blob/main/Endpoint%20Invocation.py), which makes a POST request to invoke the endpoint. The maximum request and response payload size for serverless invocations is 4 MB. As a result, the algorithm cannot take images larger than 4MB. Note that a cold start on the endpoint may delay the response time up to 4 minutes.

