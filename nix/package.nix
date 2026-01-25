{
  lib,
  python3,
}:

python3.pkgs.buildPythonPackage {
  pname = "ib_edavki";
  version = "1.4.8";
  pyproject = true;

  src = lib.cleanSource ../.;

  build-system = [ python3.pkgs.setuptools ];

  dependencies = with python3.pkgs; [
    requests
    certifi
  ];

  pythonImportsCheck = [ "ib_edavki" ];

  meta = {
    description = "Convert InteractiveBrokers XML reports to Slovenian tax forms (Doh-KDVP, D-IFI, D-Div, Doh-Obr)";
    homepage = "https://github.com/jamsix/ib-edavki";
    mainProgram = "ib_edavki";
    license = lib.licenses.mit;
  };
}
