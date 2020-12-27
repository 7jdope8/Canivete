/*
Copyright The Flagger Authors.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
*/

// Code generated by informer-gen. DO NOT EDIT.

package v1beta1

import (
	time "time"

	appmeshv1beta1 "github.com/weaveworks/flagger/pkg/apis/appmesh/v1beta1"
	versioned "github.com/weaveworks/flagger/pkg/client/clientset/versioned"
	internalinterfaces "github.com/weaveworks/flagger/pkg/client/informers/externalversions/internalinterfaces"
	v1beta1 "github.com/weaveworks/flagger/pkg/client/listers/appmesh/v1beta1"
	v1 "k8s.io/apimachinery/pkg/apis/meta/v1"
	runtime "k8s.io/apimachinery/pkg/runtime"
	watch "k8s.io/apimachinery/pkg/watch"
	cache "k8s.io/client-go/tools/cache"
)

// MeshInformer provides access to a shared informer and lister for
// Meshes.
type MeshInformer interface {
	Informer() cache.SharedIndexInformer
	Lister() v1beta1.MeshLister
}

type meshInformer struct {
	factory          internalinterfaces.SharedInformerFactory
	tweakListOptions internalinterfaces.TweakListOptionsFunc
}

// NewMeshInformer constructs a new informer for Mesh type.
// Always prefer using an informer factory to get a shared informer instead of getting an independent
// one. This reduces memory footprint and number of connections to the server.
func NewMeshInformer(client versioned.Interface, resyncPeriod time.Duration, indexers cache.Indexers) cache.SharedIndexInformer {
	return NewFilteredMeshInformer(client, resyncPeriod, indexers, nil)
}

// NewFilteredMeshInformer constructs a new informer for Mesh type.
// Always prefer using an informer factory to get a shared informer instead of getting an independent
// one. This reduces memory footprint and number of connections to the server.
func NewFilteredMeshInformer(client versioned.Interface, resyncPeriod time.Duration, indexers cache.Indexers, tweakListOptions internalinterfaces.TweakListOptionsFunc) cache.SharedIndexInformer {
	return cache.NewSharedIndexInformer(
		&cache.ListWatch{
			ListFunc: func(options v1.ListOptions) (runtime.Object, error) {
				if tweakListOptions != nil {
					tweakListOptions(&options)
				}
				return client.AppmeshV1beta1().Meshes().List(options)
			},
			WatchFunc: func(options v1.ListOptions) (watch.Interface, error) {
				if tweakListOptions != nil {
					tweakListOptions(&options)
				}
				return client.AppmeshV1beta1().Meshes().Watch(options)
			},
		},
		&appmeshv1beta1.Mesh{},
		resyncPeriod,
		indexers,
	)
}

func (f *meshInformer) defaultInformer(client versioned.Interface, resyncPeriod time.Duration) cache.SharedIndexInformer {
	return NewFilteredMeshInformer(client, resyncPeriod, cache.Indexers{cache.NamespaceIndex: cache.MetaNamespaceIndexFunc}, f.tweakListOptions)
}

func (f *meshInformer) Informer() cache.SharedIndexInformer {
	return f.factory.InformerFor(&appmeshv1beta1.Mesh{}, f.defaultInformer)
}

func (f *meshInformer) Lister() v1beta1.MeshLister {
	return v1beta1.NewMeshLister(f.Informer().GetIndexer())
}
