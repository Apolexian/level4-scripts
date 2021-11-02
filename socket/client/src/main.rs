use quic_socket::QuicListener;

fn main() {
    let addr = "0.0.0.0:4443".parse().unwrap();
    let mut listener = QuicListener::new(addr).unwrap();
    let conn_addr = "0.0.0.0:4442".parse().unwrap();
    listener.connect(conn_addr).unwrap();
    let mut conn = listener.connection.take().unwrap();
    conn.stream_send(0, b"hello", true).unwrap();
}
