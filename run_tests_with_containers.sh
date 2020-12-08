# pip install virtualenv

set +e
docker stop galaxy-test-instance
docker rm galaxy-test-instance
set -e
api_key=ahsdashdi3d3oijd23odj23
docker run -d -p 8080:80 -p 8021:21 -p 8022:22 \
    --name galaxy-test-instance \
    -e "GALAXY_CONFIG_MASTER_API_KEY=$api_key" \
    -e "GALAXY_CONFIG_ALLOW_PATH_PASTE=true" \
    -e "NONUSE=nodejs,proftp,reports" \
    -v $( pwd ):$( pwd ) \
    bgruening/galaxy-stable:19.09
rm -rf venv-test
python -m venv venv-test
source venv-test/bin/activate
pip install --upgrade pip
pip install wheel
pip install . ephemeris galaxy-parsec
galaxy-wait -g http://localhost:8080/
admin_id=$(parsec -g test -f test/parsec_creds.yaml users get_users | jq '.[] | select(.username=="admin") | .id' | sed s/\"//g)
api_key_admin=$(parsec -g test -f test/parsec_creds.yaml users create_user_apikey $admin_id)
test_dir=$( pwd )/library/tests
test_lib_def=library/tests/nfs_lib.yaml
test_creds=test/creds.yaml
sed "s+<TEMPLATE_DIR>+$test_dir+" library/tests/nfs_lib.yaml.template > $test_lib_def
sed "s/<ADMIN_USER_API_KEY>/$api_key_admin/" test/test_galaxy_credentials.yaml.template > $test_creds

python load-into-galaxy-library.py --lib-def $test_lib_def -C $test_creds -G test

parsec -g test -f test/creds.yaml libraries get_libraries