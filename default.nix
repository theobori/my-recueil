{
  lib,
  stdenvNoCC,
  recueil,
}:
stdenvNoCC.mkDerivation {
  pname = "my-recueil";
  version = "0.0.1";

  src = ./.;

  nativeBuildInputs = [
    recueil
  ];

  buildPhase = ''
    runHook preBuild

    mkdir -p ./my-recueil
    recueil build \
        --configuration "./configuration.yaml" \
        --source-directory "./my-images" \
        --destination-directory "./my-recueil" \
        --verbose

    runHook postBuild
  '';

  installPhase = ''
    runHook preInstall

    cp -r ./my-recueil $out

    runHook postInstall
  '';

  meta = {
    description = "My recueil";
    homepage = "https://github.com/theobori/my-recueil";
    license = lib.licenses.gpl3Plus;
  };
}
