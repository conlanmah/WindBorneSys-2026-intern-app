{
  description = "Simple Django project with Nix";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-25.05";
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
          railway
        ];
        pythonEnv = pkgs.python311.withPackages pythonPackages;
      in
      {
        devShells.default = pkgs.mkShell {
          buildInputs = with pkgs; [
            pythonEnv
            sqlite
          ];
          
          shellHook = ''
            echo "🚀 Django development environment ready!"
            echo "Create project: django-admin startproject myproject ."
            echo "Run migrations: python manage.py migrate"
            echo "Start server: python manage.py runserver"
          '';
          SECRET_KEY="django-insecure-*1$sy8^^5dj1_rysnpu6gjpjbfo8b0*l3o+_o3xww+4iw6_qna";
          DEBUG=1;
        };
      });
}
