from rest_framework.views import APIView
from rest_framework.response import Response 
from . import models, serializers
from rest_framework import status


# class ListAllImages(APIView):

#     def get(self, request, format=None):

#         all_images = models.Image.objects.all()

#         serializer = serializers.ImageSerializer(all_images, many=True)
        
#         return Response(data=serializer.data)

# class ListAllComments(APIView):

#     def get(self, request, format=None):
#         all_comments = models.Comment.objects.all()

#         serializer = serializers.CommentSerializer(all_comments, many=True)
        
#         return Response(data=serializer.data)

# class ListAllLikes(APIView):
       
#      def get(self, request, format=None):
#         all_likes = models.Like.objects.all()

#         serializer = serializers.LikeSerializer(all_likes, many=True)
        
#         return Response(data=serializer.data)


class Feed(APIView):

    def get(self, request, format=None):
    
        user = request.user 

        following_users = user.following.all()

        image_list =[]

        for following_user in following_users: 

            user_images = following_user.images.all()[:2]
            
            for image in user_images:

                image_list.append(image)
        
        sorted_list = sorted(image_list, key=lambda image: image.created_at, reverse=True)
        
        print(sorted_list)

        serializer =serializers.ImageSerializer(sorted_list, many=True)

        return Response(serializer.data)


class LikeImage(APIView):

    def post(self, request, id, format=None):

        user=request.user

        try:
            found_image = models.Image.objects.get(id=id)
        except models.Image.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        try:
            preexisting_like = models.Like.objects.get(
                creator=user,
                image=found_image
            )
            return Response(status=status.HTTP_304_NOT_MODIFIED)
           
        except models.Like.DoesNotExist:
            
            new_like = models.Like.objects.create(
                creator=user,
                image=found_image
            )

            new_like.save() #데이터베이스에 좋아요 만들기 

            return Response(status=status.HTTP_201_CREATED)


class UnLikeImage(APIView):

    def delete(self, request, image_id, format=None):

        user=request.user

        try:
            found_image = models.Image.objects.get(id=id)
        except models.Image.DoesNotExist:
            return Response(status=status.HTTP_404_NO_FOUND)

        try:
            preexisting_like = models.Like.objects.get(
                creator=user,
                image=found_image
             )
            preexisting_like.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)

        except models.Like.DoesNotExist:
            
            return Response(status=status.HTTP_304_NOT_MODIFIED)


class CommentOnImage(APIView):

    def post(self, request, id, format=None):
       
        user = request.user

        try:
            found_image = models.Image.objects.get(id=id)
        except models.Image.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = serializers.CommentSerializer(data=request.data)
        #print(request.data)

        if serializer.is_valid():
            
            serializer.save(creator=user, image=found_image)

            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializers.errors, status=status.HTTP_400_BAD_REQUEST)


class Comment(APIView):

    def delete(self, request, comment_id, format=None):

        user = request.user
        
        try:
            comment = models.Comment.objects.get(id=comment_id, creator=user)
            comment.delete()
            return Response(status=status.HTTP_404_NOT_FOUND)

        except models.Comment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class Search(APIView):
    
    def get(self, request, format=None):

        hashtags = request.query_params.get('hashtags', None)
        
        if hashtags is not None:
        
            hashtags = hashtags.split(",")

            images = models.Image.objects.filter(tags__name__in=hashtags).distinct()
            
            serializer = serializers.CountImageSerializer(images, many=True)

            return Response(data=serializer.data, status=status.HTTP_200_OK)

        else:
            return Response(status = status.HTTP_400_BAD_REQUEST)