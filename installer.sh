while getopts ":p:u:" opt; do
    case $opt in
        p) PROJECT_NAME="$OPTARG"
           ;;
        u) USERNAME="$OPTARG"
           ;;
        \?) echo "Opción inválida -$OPTARG" >&2
            ;;
    esac
done


git init ${PROJECT_NAME}

cd ${PROJECT_NAME}

git remote add "template" https://github.com/nanounanue/pipeline-template.git

git pull template master

echo ${PROJECT_NAME} > .project-name

hub create ${USERNAME}/${PROJECT_NAME}

git add .project-name

git commit -m "Ajustando el nombre del proyecto a ${PROJECT_NAME}"

git push origin master

git flow init -d

git checkout develop

make help

echo "############################################################################################"
echo "##                                                                                        ##"
echo "##  No olvides ejecutar 'make set_project_name' para ajustar el nombre de las carpetas    ##"
echo "##                                                                                        ##"
echo "############################################################################################"

echo ""

make info 

