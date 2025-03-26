pipeline {
    agent any

    parameters {
        string(name: 'VERSION', defaultValue: '1.0', description: 'Версия сборки')
    }
    
    stages {
        stage('Build') {
            steps {
                echo 'Собираем проект...'
                sh 'make'  // Пример (замени на свою команду)
            }
        }
        stage('Test') {
            steps {
                echo 'Запускаем тесты...'
                sh 'python -m pytest'  // Пример для Python
            }
        }
        stage('Deploy') {
            steps {
                echo "Деплоим версию ${params.VERSION}"
                // sh "deploy.sh ${params.VERSION}"  // Пример для реального деплоя
            }
        }
    }
}
