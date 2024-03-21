// rustimport:pyo3

//:
//: [dependencies]
//: rusqlite = "0.19.0"

use pyo3::prelude::*;

#[pyfunction]
fn square(n: i32) -> i32 {
    n * n * n
    // this is another comment
}