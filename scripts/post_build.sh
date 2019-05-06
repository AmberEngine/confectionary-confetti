#! /bin/bash

case $CODEBUILD_INITIATOR in
    codepipeline/Confetti)
        twine upload --username $PYPI_USERNAME \
                     --password "$PYPI_PASSWORD" \
                     --repository-url https://upload.pypi.org/legacy/ dist/*
        ;;
    codepipeline/ConfettiDevelopment)
        twine upload --username $PYPI_TESTING_USERNAME \
                     --password "$PYPI_TESTING_PASSWORD" \
                     --repository-url https://test.pypi.org/legacy/ dist/*
        ;;
esac
