from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User, Profile, Post, Comment, Like
from .serializers import UserSerializer, ProfileSerializer, PostSerializer, CommentSerializer, LikeSeraializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser

# Create your views here.

# User Registration
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def post(self, request):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')

        if not username or not password:
            return Response({"error": "Username and password are required."}, status=400)
        
        if User.objects.filter(username=username).exists():
            return Response({"error": "Username already exists."}, status=400)
        
        user = User.objects.create_user(username=username, email=email, password=password)
        Profile.objects.create(user=user)
        return Response({"message": "User registered successfully"}, status=201)
    
# Profile Management
class ProfileDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Profile.objects.all()
    serialiazer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return get_object_or_404(Profile, id=self.kwargs['id'])    

# Post CRUD
class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]  

    def get_object(self):
        post = get_object_or_404(Post, id=self.kwargs['pk'])
        
        if self.request.method in ['PUT', 'DELETE'] and post.author != self.request.user:
            self.permission_denied(self.request, message="You can only modify your own posts.")
        return post

# Like a Post
class LikePostView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        post = get_object_or_404(Post, id=id)
        like, created = Like.objects.get_or_create(user=request.user, post=post)
        if not created:
            like.delete()
            return Response({'message': 'Post unliked.'}, status=200)
        return Response({'message': 'Post liked.'}, status=201)
    
# Comment on a Post
class CommentCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        post = get_object_or_404(Post, id=id)
        text = request.data.get('text')
        if not text:
            return Response({'error': 'Comment text required.'}, status=400)
        comment = Comment.objects.create(user=request.user, post=post, text=text)
        return Response(CommentSerializer(comment).data, status=201)

    def delete(self, request, id):
        comment = get_object_or_404(Comment, id=id, user=request.user)
        comment.delete()
        return Response({'message': 'Comment deleted.'}, status=204)

# Admin Delete Any Post
class AdminDeletePostView(APIView):
    permission_classes = [IsAdminUser]

    def delete(self, request, id):
        post = get_object_or_404(Post, id=id)
        post.delete()
        return Response({'message': 'Post deleted by Admin.'}, status=204)
