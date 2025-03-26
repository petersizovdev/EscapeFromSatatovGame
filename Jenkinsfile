pipeline {
    agent any
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
    }
}
