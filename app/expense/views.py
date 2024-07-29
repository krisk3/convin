from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes
from .serializers import ExpenseSerializer, IndividualExpenseSerializer, IndividualExpenseSerializer
from .models import Expense, UserExpense




class ExpenseCreateView(APIView):
    """View to create an expense."""
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ExpenseSerializer

    def post(self, request, *args, **kwargs):
        User = get_user_model()
        serializer = ExpenseSerializer(data=request.data)
        if serializer.is_valid():

            # Split type is equal
            if serializer.validated_data['split_type'] == 'equal':
                amount_verifier = 0.0
                user = self.request.user
                user_expenses = serializer.data.get('user_expense', [])

                expense_obj = Expense.objects.create(
                    amount = serializer.validated_data['amount'],
                    split_type = serializer.validated_data['split_type'],
                    title = serializer.validated_data['title'],
                    creator = user
                )

                amt_owed = float(serializer.validated_data['amount']) / float(len(user_expenses))

                for user_expense in user_expenses:
                    email = user_expense.get('email', None)
                    mobile = user_expense.get('mobile', None)
                    input_amt = user_expense.get('amount_owed', None)
                    input_percentage = user_expense.get('percentage_owed', None)

                    if not(input_amt == None or input_amt == ""):
                        expense_obj.delete()
                        return Response({"error": "Amount owned by any user is not required as you have chosen equal split."}, status=status.HTTP_400_BAD_REQUEST)
                    if not(input_percentage == None or input_percentage == ""):
                        expense_obj.delete()
                        return Response({"error": "Percentage owned by any user is not required as you have chosen equal split."}, status=status.HTTP_400_BAD_REQUEST)

                    if email == "":
                        email = None
                    if mobile == "":
                        mobile = None

                    if email and mobile:
                        user = User.objects.filter(email=email, mobile=mobile).first()
                    elif email:
                        user = User.objects.filter(email=email).first()
                    elif mobile:
                        user = User.objects.filter(mobile=mobile).first()
                    else:
                        expense_obj.delete()
                        return Response({"error": "Email or mobile number of every user must be provided."}, status=status.HTTP_400_BAD_REQUEST)


                    UserExpense.objects.create(
                        expense = expense_obj,
                        user = user,
                        amount_owed = amt_owed
                    )
                    amount_verifier += amt_owed

                if not(amount_verifier == serializer.validated_data['amount']):
                    expense_obj.delete()
                    return Response({"error": "Amount does not match."}, status=status.HTTP_400_BAD_REQUEST)
                return Response({"message": "Expense created successfully."}, status=status.HTTP_201_CREATED)



            # Split type is exact
            elif serializer.validated_data['split_type'] == 'exact':
                amount_verifier = 0.0
                user = self.request.user
                user_expenses = serializer.data.get('user_expense', [])

                expense_obj = Expense.objects.create(
                    amount = serializer.validated_data['amount'],
                    split_type = serializer.validated_data['split_type'],
                    title = serializer.validated_data['title'],
                    creator = user
                )

                for user_expense in user_expenses:
                    email = user_expense.get('email', None)
                    mobile = user_expense.get('mobile', None)

                    if not(input_percentage == None or input_percentage == ""):
                        expense_obj.delete()
                        return Response({"error": "Percentage owned by any user is not required as you have chosen exact split."}, status=status.HTTP_400_BAD_REQUEST)

                    if email == "":
                        email = None
                    if mobile == "":
                        mobile = None

                    if email and mobile:
                        user = User.objects.filter(email=email, mobile=mobile).first()
                    elif email:
                        user = User.objects.filter(email=email).first()
                    elif mobile:
                        user = User.objects.filter(mobile=mobile).first()
                    else:
                        expense_obj.delete()
                        return Response({"error": "Email or mobile number of every user must be provided."}, status=status.HTTP_400_BAD_REQUEST)

                    amt_owed = user_expense.get('amount_owed', None)
                    if amt_owed == "" or amt_owed == None:
                        expense_obj.delete()
                        return Response({"error": "Amount owed by every user must be mentioned."}, status=status.HTTP_400_BAD_REQUEST)
                    else:
                        amt_owed = float(amt_owed)
                    amount_verifier += amt_owed

                    UserExpense.objects.create(
                        expense = expense_obj,
                        user = user,
                        amount_owed = amt_owed
                    )

                if not(amount_verifier == serializer.validated_data['amount']):
                    expense_obj.delete()
                    return Response({"error": "Amount does not match."}, status=status.HTTP_400_BAD_REQUEST)
                return Response({"message": "Expense created successfully."}, status=status.HTTP_201_CREATED)



            # Split type is percentage
            elif serializer.validated_data['split_type'] == 'percentage':
                percentage_verifier = 0.0
                amount_verifier = 0.0
                user = self.request.user
                user_expenses = serializer.data.get('user_expense', [])

                expense_obj = Expense.objects.create(
                    amount = serializer.validated_data['amount'],
                    split_type = serializer.validated_data['split_type'],
                    title = serializer.validated_data['title'],
                    creator = user
                )
                print("object created")

                total_amount = float(serializer.validated_data['amount'])

                for user_expense in user_expenses:
                    email = user_expense.get('email', None)
                    mobile = user_expense.get('mobile', None)

                    if not(input_amt == None or input_amt == ""):
                        expense_obj.delete()
                        return Response({"error": "Amount owned by any user is not required as you have chosen percentage split."}, status=status.HTTP_400_BAD_REQUEST)

                    if email == "":
                        email = None
                    if mobile == "":
                        mobile = None

                    if email and mobile:
                        user = User.objects.filter(email=email, mobile=mobile).first()
                    elif email:
                        user = User.objects.filter(email=email).first()
                    elif mobile:
                        user = User.objects.filter(mobile=mobile).first()
                    else:
                        expense_obj.delete()
                        return Response({"error": "Email or mobile number of every user must be provided."}, status=status.HTTP_400_BAD_REQUEST)

                    perc_owed = user_expense.get('percentage_owed', None)
                    if perc_owed == "" or perc_owed == None:
                        expense_obj.delete()
                        return Response({"error": "Percentage owed by every user must be mentioned."}, status=status.HTTP_400_BAD_REQUEST)
                    else:
                        perc_owed = float(perc_owed)
                        amt_owed = perc_owed*(total_amount / 100.0)
                    percentage_verifier += perc_owed
                    amount_verifier += amt_owed

                    UserExpense.objects.create(
                        expense = expense_obj,
                        user = user,
                        amount_owed = amt_owed
                    )

                if not(amount_verifier == serializer.validated_data['amount']):
                    expense_obj.delete()
                    return Response({"error": "Amount does not match."}, status=status.HTTP_400_BAD_REQUEST)
                elif not(percentage_verifier == 100):
                    expense_obj.delete()
                    return Response({"error": "Percentage does not add upto 100."}, status=status.HTTP_400_BAD_REQUEST)
                return Response({"message": "Expense created successfully."}, status=status.HTTP_201_CREATED)
            else:
                return Response({"error": "Invalid split type."}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
parameters=[
    OpenApiParameter(name='email', type=OpenApiTypes.EMAIL, description='Email of the user.', required=False,),
    OpenApiParameter(name='mobile', type=OpenApiTypes.STR, description='Mobile of the user.', required=False,),
],
responses={status.HTTP_200_OK: IndividualExpenseSerializer()})
class IndividualExpenseView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = IndividualExpenseSerializer


    def get(self, request, *args, **kwargs):
        User = get_user_model()
        email = request.query_params.get('email', None)
        mobile = request.query_params.get('mobile', None)

        if email:
            user = User.objects.filter(email=email).first()
        elif mobile:
            user = User.objects.filter(mobile=mobile).first()
        elif email and mobile:
            user = User.objects.filter(email=email, mobile=mobile).first()
        else:
            return Response({"error": "Email or mobile number must be provided."}, status=status.HTTP_400_BAD_REQUEST)


        if user:
            user_expenses = UserExpense.objects.filter(user=user)
            serializer = IndividualExpenseSerializer(user_expenses, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
