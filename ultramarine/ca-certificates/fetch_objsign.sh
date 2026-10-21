#!/bin/sh
#
# This script fetches the object signing list from the Microsoft list. It then
# mergest that list into the fetched certdata.txt.
#
giturl="https://github.com/dotnet/sdk"
gitrawurl="https://raw.githubusercontent.com/dotnet/sdk"
release="latest"
treedir="src/Layout/redist/trustedroots/codesignctl.pem"
target="microsoft_sign_obj_ca.pem"
certdata="./certdata.txt"
baseurl=""
merge=1
diff=0

function getlatest
{
    local url=$1
    local latest="0"
    local tags=($(git ls-remote --tags ${url}))
    for tag in "${tags[@]}"
    do
        if [[ ! ${tag} =~ refs/.* ]];  then
            continue # skip hashes
        fi
        if [[ ${tag} =~ .*preview.* ]];  then
            continue # skip preview tags, we only want release tags
        fi
        if [[ ${tag} =~ .*rc.* ]];  then
            continue # skip release candidate tags, we only want release tags
        fi
        if [[ ${latest} < ${tag} ]]; then
            latest=$tag
        fi
    done
    latest=${latest##refs/tags/}
    echo $latest
}

while [ -n "$1" ]; do
   case $1 in
   "-g")
        shift
	giturl=$1
	;;
   "-r")
        shift
	gitrawurl=$1
	;;
   "-t")
        shift
	treedir=$1
	;;
   "-r")
        shift
	release=$1
	;;
   "-u")
        shift
	baseurl=$1
        release="unknown"
	;;
   "-o")
        shift
	target=$1
	;;
   "-c")
        shift
	certdata=$1
	;;
   "-n")
        merge=0
        ;;
   "-d")
        shift
        diff=1
        difffile=$1
        ;;
    *)
	echo "usage: $0 [-u URL] [-o target] [-c certdata] [-n]"
	echo "-g URL      git URL to fetch code signing list"
	echo "-r URL      raw git URL to fetch code signing list"
	echo "-t URL      git tree directory to fetch code signing list"
	echo "-r release  code signing list release version"
	echo "-u URL      base URL to fetch code signing list"
	echo "-o target   name of the codesigning target"
	echo "-c certdata patch to certdata.txt to merge with"
	echo "-d diff     optional diff file"
        echo "-n          don't merge"
	exit 1
	;;
    esac
    shift
done

if [ "${release}" = "latest" ]; then
     release=$(getlatest ${giturl} )
fi

if [ "${baseurl}" = "" ]; then
     baseurl="${gitrawurl}/${release}/${treedir}"
fi

echo $release > "./codesign-release.txt"

echo "Fetching release=${release}, ${target} from ${baseurl}"

wget ${baseurl} -O ${target}

if [ ${merge} -eq 0 ]; then
    exit 0;
fi

out=${certdata}
if [ ${diff} -eq 1 ]; then
   out=${certdata}.out
fi
python3 ./mergepem2certdata.py -c "${certdata}" -p "${target}" -o "${out}" -t "CKA_TRUST_CODE_SIGNING" -l "Microsoft Code Signing Only Certificate"

if [ ${diff} -eq 1 ]; then
    diff -u ${certdata} ${out} > ${difffile}
    mv ${out} ${certdata}
fi
