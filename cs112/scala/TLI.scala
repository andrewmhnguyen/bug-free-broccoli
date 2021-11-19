/*
This program was completed using pair programming by
Andrew Nguyen, anguy224@ucsc.edu and Kenneth Nguyen, knguy149@ucsc.edu
I acknowledge that each partner in a programming pair should "drive"
roughly 50% of the time the pair is working together, and at most 25%
of an individual's effort for an assignment should be spent working
alone. Any work done by a solitary programmer must be reviewed by the
partner. The object is to work together, learning from each other, not
to divide the work into two pieces with each partner working on a
different piece.
We are both submitting the same program.
*/

import scala.collection.mutable.Map
import scala.io.Source

abstract class Expr
case class Var(name: String) extends Expr
case class Str(name: String) extends Expr
case class Constant(num: Double) extends Expr
case class BinOp(operator: String, left: Expr, right: Expr) extends Expr

abstract class Stmt
case class Let(variable: String, expr: Expr) extends Stmt
case class If(expr: Expr, label: String) extends Stmt
case class Input(variable: String) extends Stmt
case class Print(exprList: List[Expr]) extends Stmt

object TLI {
    def eval(expr: Expr, symTab: Map[String, Double]): Double = expr match {
        case BinOp("+",e1,e2) => eval(e1,symTab) + eval(e2,symTab)
        case BinOp("-",e1,e2) => eval(e1,symTab) - eval(e2,symTab)
        case BinOp("*",e1,e2) => eval(e1,symTab) * eval(e2,symTab)
        case BinOp("/",e1,e2) => eval(e1,symTab) / eval(e2,symTab)
        case BinOp("<",e1,e2) => if (eval(e1,symTab) < eval(e2,symTab)) 1 else 0
        case BinOp(">",e1,e2) => if (eval(e1,symTab) > eval(e2,symTab)) 1 else 0
        case BinOp("<=",e1,e2) => if (eval(e1,symTab) <= eval(e2,symTab)) 1 else 0
        case BinOp(">=",e1,e2) => if (eval(e1,symTab) >= eval(e2,symTab)) 1 else 0
        case BinOp("==",e1,e2) => if (eval(e1,symTab) == eval(e2,symTab)) 1 else 0 
        case BinOp("!=",e1,e2) => if (eval(e1,symTab) != eval(e2,symTab)) 1 else 0
        case Var(name) => symTab(name)
        case Constant(num) => num
	case _ => throw new Exception("Error") // should really throw an error
    }

    def parseLet(text: Array[String], symTab: Map[String, Double]): Expr = {
        var variable = text.slice(1,2) // get the variable of Let stmt
        var textLength = text.length // determine whether the Let stmt has a BinOp
        textLength match {
            // case is if the Let stmt has only a variable or constant
            case 4 => {
                var expression = text.slice(3, 4) // get the expression to the right of the "="
                if ((expression(0).forall(_.isLetter))) { // expression is a variable
                    symTab += (variable(0) -> eval(Var(expression(0)), symTab)) 
                    Var(expression(0))
                }
                else if ((expression(0).forall(_.isDigit))) { // expression is a constant
                    symTab += (variable(0) -> eval(Constant(expression(0).toDouble), symTab))
                    Constant(expression(0).toDouble)
                }
                else {
                    throw new Exception("Error")
                }
            }
            // case is if the Let stmt has a binary operator
            case 6 => {
               var expression = text.slice(3, 6) // get the expression to the right of the "="
               var left = expression.slice(0,1) // left of the operator sign
               var operator = expression.slice(1,2) // operator sign
               var right = expression.slice(2,3) // right of the operator sign
               var leftVar = false // determine if the left is a variable
               var rightVar = false // determine if the right is a variable
               if (left(0).forall(_.isLetter) && right(0).forall(_.isLetter)) {
                   leftVar = true
                   rightVar = true
               }
               else if (left(0).forall(_.isLetter) && right(0).forall(_.isDigit)) {
                   leftVar = true
                   rightVar = false
               }
               else if (left(0).forall(_.isDigit) && right(0).forall(_.isLetter)) {
                   leftVar = false
                   rightVar = true
               }
               else if (left(0).forall(_.isDigit) && right(0).forall(_.isDigit)) {
                   leftVar = false
                   rightVar = false
               }
               // update symbol table accordingly depending on the Expr of the right and left
               if (leftVar && rightVar) {
                   var leftValue = Var(left(0))
                   var rightValue = Var(right(0))
                   symTab += (variable(0) -> eval(BinOp(operator(0), leftValue, rightValue), symTab))
                   BinOp(operator(0), leftValue, rightValue)
               }
               else if (!leftVar && rightVar) {
                    var leftValue = Constant(left(0).toDouble)
                    var rightValue = Var(right(0))
                    symTab += (variable(0) -> eval(BinOp(operator(0), leftValue, rightValue), symTab))
                    BinOp(operator(0), leftValue, rightValue)
               }
               else if (leftVar && !rightVar) {
                    var leftValue = Var(left(0))
                    var rightValue = Constant(right(0).toDouble)
                    symTab += (variable(0) -> eval(BinOp(operator(0), leftValue, rightValue), symTab))
                    BinOp(operator(0), leftValue, rightValue)
               }
               else if (!leftVar && !rightVar){
                   var leftValue = Constant(left(0).toDouble)
                   var rightValue = Constant(right(0).toDouble)
                   symTab += (variable(0) -> eval(BinOp(operator(0), leftValue, rightValue), symTab))
                   BinOp(operator(0), leftValue, rightValue)
               }
               else {
                   throw new Exception("Error")
               }
            }

            case _ => throw new Exception("Error")
        }  
    }

    def parsePrint(text: String, symTab: Map[String, Double]): List[Expr] = {
        var printList: List[Expr] = List()
        var splitComma = text.split(",") // remove all instances of the comma
        splitComma(0) = splitComma(0).replace("print ", "") // exclude "print" keyword
        for (i <- 0 to splitComma.length - 1) {
            var trimExpr = splitComma(i).trim() // trim left and right whitespace
            // if the variable already exists in the symbol table
            if (symTab contains trimExpr) {
                printList = printList :+ Var(trimExpr) 
                print(symTab(trimExpr) + " ")
            }
            // if the current element is a string constant
            else if (trimExpr.charAt(0) == '"' && trimExpr.charAt(trimExpr.length-1) == '"') {
                printList = printList :+ Str(trimExpr)
                print(trimExpr.replaceAll("\"", "") + " ")
            }
            // if the current element is a binary operator
            else {
                // same logic as in parseLet for a binary operator
                var binArray = trimExpr.split(" ")
                var left = binArray.slice(0,1)
                var operator = binArray.slice(1,2)
                var right = binArray.slice(2,3)
                var leftVar = false
                var rightVar = false
                if (left(0).forall(_.isLetter) && right(0).forall(_.isLetter)) {
                    leftVar = true
                    rightVar = true
                }
                else if (left(0).forall(_.isLetter) && right(0).forall(_.isDigit)) {
                    leftVar = true
                    rightVar = false
                }
                else if (left(0).forall(_.isDigit) && right(0).forall(_.isLetter)) {
                    leftVar = false
                    rightVar = true
                }
                else if (left(0).forall(_.isDigit) && right(0).forall(_.isDigit)) {
                    leftVar = false
                    rightVar = false
                }
                
                if (leftVar && rightVar) {
                    var leftValue = Var(left(0))
                    var rightValue = Var(right(0))
                    printList = printList :+ BinOp(operator(0), leftValue, rightValue)
                    print(eval(BinOp(operator(0), leftValue, rightValue), symTab) + " ")
                }
                else if (!leftVar && rightVar) {
                        var leftValue = Constant(left(0).toDouble)
                        var rightValue = Var(right(0))
                        printList = printList :+ BinOp(operator(0), leftValue, rightValue)
                        print(eval(BinOp(operator(0), leftValue, rightValue), symTab) + " ")
                }
                else if (leftVar && !rightVar) {
                        var leftValue = Var(left(0))
                        var rightValue = Constant(right(0).toDouble)
                        printList = printList :+ BinOp(operator(0), leftValue, rightValue)
                        print(eval(BinOp(operator(0), leftValue, rightValue), symTab) + " ")
                }
                else if (!leftVar && !rightVar){
                    var leftValue = Constant(left(0).toDouble)
                    var rightValue = Constant(right(0).toDouble)
                    printList = printList :+ BinOp(operator(0), leftValue, rightValue)
                    print(eval(BinOp(operator(0), leftValue, rightValue), symTab) + " ")
                }                
            }
        }
        printList
    } 

    def main(args: Array[String]) {
        // list of Stmt objects
        var statementList: List[Stmt] = List()

        // symbol table stores variable/label mappings
        var symTable = Map[String, Double]()
        
        // parse each line to a Stmt object
        for (line <- Source.fromFile(args(0)).getLines()) {
            //println(line)
            var splitLine = line.split("\\s+")
            var stmtKey = splitLine(0)
            var stmt = stmtKey match {
                case "let" => {
                    var variable = splitLine(1)
                    var expr = parseLet(splitLine, symTable)
                    statementList = statementList :+ Let(variable, expr)
                }
                case "print" => {
                    var exprList = parsePrint(line, symTable)
                    println("")
                    statementList = statementList :+ Print(exprList)
                }
                case _ => throw new Exception("Error")
            }
        }
    }
}