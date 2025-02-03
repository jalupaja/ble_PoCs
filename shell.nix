{ pkgs ? import <nixpkgs> {} }:

# Define the environment
pkgs.mkShell {
  buildInputs = with pkgs;[
    python312
    python312Packages.bleak
  ];
}
