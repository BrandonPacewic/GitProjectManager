// Copyright (c) Brandon Pacewic
// SPDX-License-Identifier: MIT

struct Color<'a> {
    console_code: &'a str
}

use clap::Parser;

#[derive(Parser, Debug)]
#[clap(author, version, about, long_about = None)]
struct Cli {
    #[clap(short, long, value_parser)]
    project_name: String,
}

fn main() {
    let green = Color { console_code: "\033[92m" };
    let red = Color { console_code: "\033[91m" };
    let yellow = Color { console_code: "\033[93m" };
    let reset = Color { console_code: "\033[0m" };

    let args = Cli::parse();

    println!("{}Hello, {}!{}", green.console_code, args.project_name, reset.console_code);
}