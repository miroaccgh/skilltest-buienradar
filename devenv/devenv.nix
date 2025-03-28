{pkgs, ... }:
# Declarition for reproducible dev environment

{
  packages = with pkgs; [
    python310
    poetry
  ];
  enterShell = ''
    cd ../
  '';

}
