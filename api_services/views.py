from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from api_services.models import Tasks, Files, Comments
from api_services.serializers import TasksSerializer, FilesSerializer, CommentsSerializer


# api view functions for tasks
@api_view(['GET', 'POST'])
def task_list(request):

    if request.method == 'GET':
        snippets = Tasks.objects.all()
        serializer = TasksSerializer(snippets, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = TasksSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def task_detail(request, pk):
    try:
        task_detail = Tasks.objects.get(pk=pk)
    except Tasks.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = TasksSerializer(task_detail)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = TasksSerializer(task_detail, data=request.data)
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
        snippets = Files.objects.all()
        serializer = FilesSerializer(snippets, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = FilesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def file_detail(request, pk):
    try:
        file_details = Files.objects.get(pk=pk)
    except Files.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = FilesSerializer(file_details)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = FilesSerializer(file_details, data=request.data)
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
        snippets = Comments.objects.all()
        serializer = CommentsSerializer(snippets, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = CommentsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



