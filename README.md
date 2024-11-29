# **Server and Client Simulation**

## **Project Overview**  
This project demonstrates the use of the TCP/IP stack to illustrate how transport layer protocols facilitate data transmission across networks. It showcases two primary modes of communication:  
1. **Client-to-Client (Peer-to-Peer)**  
2. **Client-to-Server**

The implementation utilizes both **TCP** and **UDP** protocols to highlight their distinct roles in network communication.

## **Features**  
- **TCP (Transmission Control Protocol)**:  
  - A connection-oriented protocol used for reliable communication between the client and the server.  
  - Ensures data integrity and delivery by establishing a secure connection before data transfer.

- **UDP (User Datagram Protocol)**:  
  - A connectionless protocol employed for peer-to-peer communication.  
  - Focuses on speed and efficiency, making it ideal for scenarios where reliability is less critical.

## **How It Works**  
1. **Client-to-Server Communication**:  
   - The client establishes a connection to the server using TCP.  
   - Data packets are exchanged with a guarantee of reliability and order.  

2. **Peer-to-Peer Communication**:  
   - The client communicates with other clients using UDP.  
   - This allows fast and lightweight transmission without the overhead of establishing and maintaining a connection.

## **Use Cases**  
- Understanding the roles of TCP and UDP in network communication.  
- Simulating client-server and peer-to-peer interactions in a controlled environment.  
- Educational purposes to explore the differences between connection-oriented and connectionless protocols.

## **Technical Details**  
- **Transport Layer Protocols**:  
  - TCP: Provides error-checking, acknowledgment, and data reordering for reliable communication.  
  - UDP: Offers low-latency communication without the need for connection setup.  

- **Network Stack**:  
  - Based on the TCP/IP model to demonstrate real-world transport mechanisms.  
