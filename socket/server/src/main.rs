use quic_socket::QuicSocket;
use tokio;

#[tokio::main]
async fn main() {
    let addr = "0.0.0.0:4444".parse().unwrap();
    let socket = QuicSocket::bind(addr).await.unwrap();
    let acc_addr = "0.0.0.0:4443".parse().unwrap();
    let mut listener = socket.accept(acc_addr).unwrap();
    let mut buf = [0; 65535];
    let read = match listener.recv(&mut buf).await {
        Ok(r) => r,
        Err(e) => {
            println!("{:?}", e);
            return;
        }
    };
    println!("{:?}", &buf[..read]);
}
