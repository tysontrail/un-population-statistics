{
  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable-small";
  };
  outputs = inputs: let
    system = "x86_64-linux";
    nixpkgs = import inputs.nixpkgs {inherit system;};
  in {
    packages.${system} = {
      default = nixpkgs.writeShellScriptBin "main" ''
        ${nixpkgs.python39.withPackages (_: [
          nixpkgs.python39Packages.matplotlib
          nixpkgs.python39Packages.numpy
          nixpkgs.python39Packages.pandas
          nixpkgs.python39Packages.openpyxl
        ])}/bin/python ${./main.py}
      '';
      container = nixpkgs.dockerTools.buildLayeredImage {
        name = "kernel-panic";
        tag = "latest";

        config = {
          Entrypoint = "${inputs.self.packages.${system}.default}/bin/main";
          WorkingDir = "/data";
        };
      };
    };
  };
}
