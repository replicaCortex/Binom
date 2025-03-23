{
  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = {
    nixpkgs,
    flake-utils,
    ...
  }:
    flake-utils.lib.eachDefaultSystem (
      system: let
        pkgs = import nixpkgs {inherit system;};
        pythonEnv = pkgs.python312.withPackages (ps:
          with ps; [
            ipython
            ipykernel
            jupyter
            numpy
            pytest
            matplotlib
            scipy
            cookiecutter
            pandas
            pip
            seaborn
            catppuccin
            scikit-learn
            tqdm
          ]);
      in {
        devShell = pkgs.mkShell {
          buildInputs = with pkgs; [
            pythonEnv
          ];

          shellHook = ''
            # явно экспортируем PYTHONPATH

            python -m ipykernel install --user --name my_kernel --display-name "Python (my_kernel)"

            export PYTHONPATH="${pythonEnv}:$PYTHONPATH:${pythonEnv}/${pythonEnv.sitePackages}"

            trap 'jupyter kernelspec remove -y my_kernel' EXIT

            exec zsh
          '';
        };
      }
    );
}
