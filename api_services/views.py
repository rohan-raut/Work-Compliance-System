from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from api_services.models import Task, File, Comment
from api_services.serializers import TaskSerializer, FileSerializer, CommentSerializer, AccountSerializer
from rest_framework.authtoken.models import Token
from api_services.filters import TaskFilter 


# api view functions for tasks
@api_view(['GET', 'POST'])
def task_list(request):

    if request.method == 'GET':
        snippets = Task.objects.all()
        filterset = TaskFilter(request.GET, queryset=snippets)
        if filterset.is_valid():
            snippets = filterset.qs
        serializer = TaskSerializer(snippets, many=True)   
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def task_detail(request, pk):
    try:
        task_detail = Task.objects.get(pk=pk)
    except Task.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = TaskSerializer(task_detail)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = TaskSerializer(task_detail, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        task_detail.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



# api view functions for files
@api_view(['GET', 'POST'])
def file_list(request):

    if request.method == 'GET':
        snippets = File.objects.all()
        serializer = FileSerializer(snippets, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = FileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def file_detail(request, pk):
    try:
        file_details = File.objects.get(pk=pk)
    except File.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = FileSerializer(file_details)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = FileSerializer(file_details, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        file_details.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# api view functions for comments
@api_view(['GET', 'POST'])
def comment_list(request):

    if request.method == 'GET':
        snippets = Comment.objects.all()
        serializer = CommentSerializer(snippets, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST',])
def registration_view(request):
    if request.method == 'POST':
        serializer = AccountSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            account = serializer.save()
            data['response'] = 'Successfully registered a new user.'
            data['email'] = account.email
            data['first_name'] = account.first_name
            data['last_name'] = account.last_name
            data['user_role'] = account.user_role
            token = Token.objects.get(user=account).key
            data['token'] = token
        else:
            data = serializer.errors
        return Response(data)
