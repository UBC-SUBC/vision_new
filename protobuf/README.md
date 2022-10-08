# SUBC Google Protobuf Guide

[Protocol buffers](https://developers.google.com/protocol-buffers/) are Google's language-neutral, platform-neutral, extensible mechanism for serializing structured data – think XML, but smaller, faster, and simpler. At SUBC we use protocol buffers to communicate across various sub systems that may or may not be programmed in different programming languages. Protobufs allows us to write data structures that can easily be encoded or decoded to bytes and understood in our different subsytems using the generated output files. 

## Set up

Many of our subsystems are running with microcontrollers that are very memory limited. Thus, we use [nanopb](https://github.com/nanopb/nanopb) for its smaller header size and improved memory usage. To install the required tools for using nanopb you must first clone the repository by using the command: 

```
git clone https://github.com/nanopb/nanopb.git
```

Within said repository there should be a MakeFile in the ```examples/simple``` directory that you can use to familiarize yourself with protocol buffers and how they function. To run the example, enter the repository and enter the command:

```
make
```

Alternatively, within the subc repository you can navigate to the ```protobuf``` repository and view my slighly worst example with the compiled VisionDAQ communication ;) **Note**: you may have to set an environment variable for this to work. In linux you can enter the command (should be similar on mac):

```
export PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python
```

## Writing Structures with Protobufs

Google protobuf uses a c-like syntax to define its structures. You will start by writing your structure in the protobuf language in a .proto file and then will run the protoc compiler to compile it to the language of your choice. This process will automatically generate the files you need to access the structure in your desired language and encode or decode it to and from bytes. For documentation and examples of protobuf syntax, see this [link](https://developers.google.com/protocol-buffers/docs/proto). 