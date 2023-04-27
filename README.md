<div id="top"></div>

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <h1 align="center">Raft Consensus</h1>
</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#about-the-project">About The Project</a></li>
    <li><a href="#built-with">Built With</a></li>
    <li><a href="#getting-started">Getting Started</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->

## About The Project

An implementation of the raft consensus algorithm that includes:

- Leader Election
- Log replication
- Simple Client for testing

<p align="right">(<a href="#top">back to top</a>)</p>

## Built With

- [Python](https://www.python.org/)
- [Protobuf](https://protobuf.dev/)
- [gRPC](https://grpc.io/)

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- GETTING STARTED -->

## Getting Started

#### Dependencies

First you will need to install the dependencies in the requirements.txt file by running the following command in your terminal.

```
pip install -r requirements.txt
```

Then run the following code in the terminal

```
python3 -m grpc_tools.protoc raft.proto --proto_path=. --python_out=. --grpc_python_out=.
```

#### Testing

For testing you need to update the `Config.conf` file with the desired server addresses and ports.
It follows the following schema: `[id] [address] [port]`
Then you can run multiple servers in different terminals, for example:

```
TODO
```

Each server terminal will print updates regarding its state `[Follower, Candidate, Leader]`

To test the Log replication functionality you will need to run `client.py` and interact with nodes using the following commands: `[connect, getleader, suspend, quit, getval, setval]`, for example:

```
TODO
```

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- LICENSE -->

## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- CONTACT -->

## Contact

Mosab Mohamed - [@IVIosab](https://t.me/IVIosab) - mosab.f.r@gmail.com

Project Link: [https://github.com/IVIosab/raft](https://github.com/IVIosab/raft)

<p align="right">(<a href="#top">back to top</a>)</p>
