{ pkgs ? import <nixpkgs> {} }:

let
  libPath = pkgs.lib.makeLibraryPath [
    pkgs.stdenv.cc.cc
    pkgs.zlib
  ];
in

pkgs.mkShell {
  buildInputs = [
    pkgs.python311
    pkgs.python311Packages.pip
    pkgs.python311Packages.virtualenv
    pkgs.gcc
    pkgs.zlib
  ];

  shellHook = ''
    export LD_LIBRARY_PATH=${libPath}:$LD_LIBRARY_PATH
    echo "LD_LIBRARY_PATH patched for libstdc++ and libz.so.1"
  '';
}
