{
  description = "Development shell for WindBorne Application Django project";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
        pythonPackages = ps: with ps; [
          django
          gunicorn
          whitenoise
          pytest
          black
          python-decouple
          requests
        ];
        pythonEnv = pkgs.python312.withPackages pythonPackages;
      in
      {
        devShells.default = pkgs.mkShell {
          buildInputs = with pkgs; [
            pythonEnv
            sqlite
            railway # Need the most up to date version, which is in unstable.
          ];
          
          shellHook = ''
            echo "🚀 Django development environment ready!"
            echo "Create project: django-admin startproject myproject ."
            echo "Run migrations: python manage.py migrate"
            echo "Start server: python manage.py runserver"
          '';
        };
      });
}
