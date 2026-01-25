{
  description = "InteractiveBrokers -> FURS eDavki converter";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs =
    {
      self,
      nixpkgs,
      flake-utils,
    }:
    flake-utils.lib.eachDefaultSystem (
      system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
        ib-edavki = pkgs.callPackage ./nix/package.nix { };
      in
      {
        packages = {
          ib-edavki = ib-edavki;
          default = ib-edavki;
        };

        devShells.default = pkgs.mkShell {
          buildInputs = [ ib-edavki ];
        };
      }
    );
}
