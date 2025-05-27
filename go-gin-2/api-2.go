// source: https://pkg.go.dev/go.mongodb.org/mongo-driver/mongo

package main

import (
	"context"
	"fmt"
	"time"

	"github.com/gin-gonic/gin"
	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"
)

var collection *mongo.Collection
var ctx = context.TODO()

func main() {

	router := gin.Default()

	router.GET("/user/:name", func(c *gin.Context) {

		world, _ := c.Cookie("world")

		ctx, cancel := context.WithTimeout(context.Background(), 20*time.Second)
		defer cancel()
		client, _ := mongo.Connect(ctx, options.Client().ApplyURI("mongodb://foo:bar@localhost:27017"))

		collection := client.Database("baz").Collection("qux")

		//ruleid: gin-mongo-nosqli-taint
		res, _ := collection.InsertOne(context.Background(), bson.M{"hello": world})
		fmt.Println(res)

		result := struct {
			Foo string
			Bar int32
		}{}

		filter := bson.D{{"hello", world}}
		//ruleid: gin-mongo-nosqli-taint
		collection.FindOne(context.Background(), filter).Decode(&result)

		//ruleid: gin-mongo-nosqli-taint
		res, _ = collection.InsertOne(context.Background(), bson.M{"hello": result.Foo})

	})

}

func goodstuff() {

	router := gin.Default()

	router.GET("/user/:name", func(c *gin.Context) {

		world := "world"

		ctx, cancel := context.WithTimeout(context.Background(), 20*time.Second)
		defer cancel()
		client, _ := mongo.Connect(ctx, options.Client().ApplyURI("mongodb://foo:bar@localhost:27017"))

		collection := client.Database("baz").Collection("qux")

		//ok: gin-mongo-nosqli-taint
		res, _ := collection.InsertOne(context.Background(), bson.M{"hello": world})

		fmt.Println(res)

		result := struct {
			Foo string
			Bar int32
		}{}

		filter := bson.D{{"hello", world}}
		//ok: gin-mongo-nosqli-taint
		collection.FindOne(context.Background(), filter).Decode(&result)

		//ok: gin-mongo-nosqli-taint
		res, _ = collection.InsertOne(context.Background(), bson.M{"hello": result.Foo})
		fmt.Println(res)

	})
}
