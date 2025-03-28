{pkgs, ... }:
# Declarition for reproducible dev environment

{
  packages = with pkgs; [
    poetry
  ];
  languages.python.enable = true;
  languages.python.version = "3.12";
  enterShell = ''
    cd ../
  '';
}
